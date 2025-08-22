

#----------------------------------------
# pip install psycopg2-binary
# usage:
# python compare_schemas.py \
#   --dsn "host=127.0.0.1 dbname=mydb user=myuser password=secret" \
#   --schema1 old_schema \
#   --schema2 new_schema \
#   --tables gastnr genstat res_line reservation \
#   --mode both \
#   --batch-size 10000 \
#   --only-hash
#
# For loop timing only:
# python compare_schemas.py --dsn "...dsn..." --schema1 s1 --schema2 s2 --mode time-loop --only-hash
# python compare_schemas.py --dsn "host=psql.staging.e1-vhp.com dbname=qctest user=postgres password=DevPostgreSQL#2024 port=5432" --schema1 qcserverless2 --schema2 qcserverless3 --mode time-loop --only-hash --batch-size 1000


#
# For DB‑side checksum only:
# python compare_schemas.py --dsn "...dsn..." --schema1 s1 --schema2 s2 --mode checksum
#----------------------------------------
#!/usr/bin/env python3
import argparse, time, sys
from typing import List, Tuple, Optional
import psycopg2
import psycopg2.extras

# ---------- Identifier quoting ----------

def psql_ident(ident: str) -> str:
    if not isinstance(ident, str):
        raise TypeError(f"psql_ident expected str, got {type(ident).__name__}: {ident!r}")
    return '"' + ident.replace('"', '""') + '"'

# ---------- Introspection ----------

def get_columns_with_types(conn, schema: str, table: str) -> List[Tuple[str, bool]]:
    """
    Returns list of (column_name, is_bytea) ordered by ordinal_position.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.column_name,
                   (c.udt_name = 'bytea') AS is_bytea
            FROM information_schema.columns c
            WHERE c.table_schema = %s AND c.table_name = %s
            ORDER BY c.ordinal_position
        """, (schema, table))
        rows = cur.fetchall()
        if not rows:
            raise RuntimeError(f"No columns found for {schema}.{table}")
        return [(r[0], bool(r[1])) for r in rows]

def get_primary_key(conn, schema: str, table: str) -> Optional[List[str]]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.attname
            FROM pg_index i
            JOIN pg_class c ON c.oid = i.indrelid
            JOIN pg_namespace n ON n.oid = c.relnamespace
            JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = ANY(i.indkey)
            WHERE n.nspname = %s AND c.relname = %s AND i.indisprimary
            ORDER BY array_position(i.indkey, a.attnum)
        """, (schema, table))
        rows = cur.fetchall()
        return [r[0] for r in rows] if rows else None

# ---------- Expression builders (value-only hashing; ignore field names) ----------

def make_value_expr(col: str, is_bytea: bool) -> str:
    # bytea -> hex string; everything else -> ::text
    return (f"encode({psql_ident(col)}, 'hex')" if is_bytea
            else f"{psql_ident(col)}::text")

def make_rowconcat_sql(cols_with_types):
    # Build a '||'-joined string from all column values (ignores names).
    parts = [f"COALESCE({make_value_expr(c, isb)}, '')" for c, isb in cols_with_types]
    return "array_to_string(ARRAY[" + ", ".join(parts) + "], '||')"

def make_rowhash_sql(cols_with_types):
    # md5 of the joined values
    return "md5(" + make_rowconcat_sql(cols_with_types) + ")"
# ---------- Modes ----------

def time_loop(conn, schema: str, table: str, batch_size: int, only_hash: bool):
    cols_with_types = get_columns_with_types(conn, schema, table)
    rowhash_expr = make_rowhash_sql(cols_with_types)

    select_list = rowhash_expr if only_hash else (
        rowhash_expr + ", " + ", ".join(psql_ident(c) for c, _ in cols_with_types)
    )
    order_cols = get_primary_key(conn, schema, table) or [c for c, _ in cols_with_types]
    order_by = ", ".join(psql_ident(c) for c in order_cols)

    # Set work_mem in a separate (non-named) cursor BEFORE opening the named cursor
    with conn.cursor() as cur_tmp:
        cur_tmp.execute("SET LOCAL work_mem = '128MB'")

    cur_name = f"csr_{schema}_{table}_{int(time.time()*1000)}"
    cur = conn.cursor(name=cur_name, cursor_factory=psycopg2.extras.DictCursor)
    cur.itersize = batch_size

    cur.execute(f"""
        SELECT {select_list}
        FROM {psql_ident(schema)}.{psql_ident(table)}
        ORDER BY {order_by}
    """)

    start = time.perf_counter()
    rows = 0
    checksum64 = 0
    while True:
        batch = cur.fetchmany(batch_size)
        if not batch:
            break
        for r in batch:
            # r[0] is md5 hex string -> fold into uint64 rolling checksum
            h = int(r[0], 16)
            checksum64 ^= (h & ((1<<64)-1))
            rows += 1
    elapsed = time.perf_counter() - start
    cur.close()
    return rows, elapsed, checksum64

def sql_checksum(conn, schema: str, table: str):
    cols_with_types = get_columns_with_types(conn, schema, table)
    rowconcat = make_rowconcat_sql(cols_with_types)
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT COUNT(*)::bigint,
                   SUM(hashtextextended({rowconcat}, 0))::bigint
            FROM {psql_ident(schema)}.{psql_ident(table)}
        """)
        cnt, sumh = cur.fetchone()
        return int(cnt), int(sumh or 0)

# ---------- App ----------

def main():
    parser = argparse.ArgumentParser(description="Compare performance and (optionally) content between two PostgreSQL schemas.")
    parser.add_argument("--dsn", required=True, help="psycopg2 DSN, e.g. 'host=... dbname=... user=... password=... sslmode=prefer'")
    parser.add_argument("--schema1", required=True)
    parser.add_argument("--schema2", required=True)
    parser.add_argument("--tables", nargs="+", default=["guest", "genstat", "res_line", "reservation"])
    parser.add_argument("--batch-size", type=int, default=5000)
    parser.add_argument("--mode", choices=["time-loop", "checksum", "both"], default="both")
    parser.add_argument("--only-hash", action="store_true")
    args = parser.parse_args()

    try:
        conn = psycopg2.connect(args.dsn)
        conn.autocommit = False  # needed for SET LOCAL

        print(f"Schemas: {args.schema1} vs {args.schema2}")
        print(f"Tables: {', '.join(args.tables)}")
        print(f"Mode: {args.mode} | batch={args.batch_size} | only_hash={args.only_hash}")
        print()

        for tbl in args.tables:
            print(f"=== {tbl} ===")
            if args.mode in ("time-loop", "both"):
                with conn:
                    rows1, t1, c1 = time_loop(conn, args.schema1, tbl, args.batch_size, args.only_hash)
                with conn:
                    rows2, t2, c2 = time_loop(conn, args.schema2, tbl, args.batch_size, args.only_hash)

                note = " (DIFF rowcount!)" if rows1 != rows2 else ""
                equal_hint = "equal" if (rows1 == rows2 and c1 == c2) else "DIFF"

                print(f" time-loop: {args.schema1}: rows={rows1:,} time={t1:.2f}s speed={rows1/max(t1,1e-9):,.0f} r/s checksum64=0x{c1:016x}")
                print(f"            {args.schema2}: rows={rows2:,} time={t2:.2f}s speed={rows2/max(t2,1e-9):,.0f} r/s checksum64=0x{c2:016x}{note}")
                print(f"            checksum compare: {equal_hint}")
            if args.mode in ("checksum", "both"):
                cnt1, sum1 = sql_checksum(conn, args.schema1, tbl)
                cnt2, sum2 = sql_checksum(conn, args.schema2, tbl)
                equal2 = "equal" if (cnt1 == cnt2 and sum1 == sum2) else "DIFF"
                print(f" checksum:  {args.schema1}: rows={cnt1:,} sum_hash64={sum1}")
                print(f"            {args.schema2}: rows={cnt2:,} sum_hash64={sum2}")
                print(f"            checksum compare: {equal2}")
            print()

        conn.close()
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
