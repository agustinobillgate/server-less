

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
#
# For DB‑side checksum only:
# python compare_schemas.py --dsn "...dsn..." --schema1 s1 --schema2 s2 --mode checksum
#----------------------------------------

#!/usr/bin/env python3
import argparse, time, sys
from typing import List, Tuple, Optional
import psycopg2
import psycopg2.extras

# ---------- Helpers ----------

def get_columns(conn, schema: str, table: str) -> List[str]:
    """Return column names ordered by ordinal_position."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema=%s AND table_name=%s
            ORDER BY ordinal_position
        """, (schema, table))
        cols = [r[0] for r in cur.fetchall()]
        if not cols:
            raise RuntimeError(f"No columns found for {schema}.{table}")
        return cols

def get_primary_key(conn, schema: str, table: str) -> Optional[List[str]]:
    """Return PK column list if exists, else None."""
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

def make_rowhash_sql(cols: List[str]) -> str:
    """
    Build an expression that hashes the *values* in column order, ignoring names.
    Uses md5(concat_ws(...)) which is stable across schemas as long as data and column order match.
    """
    pieces = [f"COALESCE({psql_cast(c)}, '')" for c in cols]
    return f"md5(concat_ws('||', {', '.join(pieces)}))"

def psql_cast(col: str) -> str:
    # Cast every column to text in a reasonably safe way
    # (bytea -> hex, json/jsonb -> text, arrays -> text, others -> text)
    return f"CASE WHEN pg_typeof({psql_ident(col)})::text='bytea' THEN encode({psql_ident(col)}, 'hex') ELSE {psql_ident(col)}::text END"

def psql_ident(ident: str) -> str:
    # naive identifier quoting (no dots here since we pass bare column names)
    return '"' + ident.replace('"', '""') + '"'

# ---------- Modes ----------

def time_loop(conn, schema: str, table: str, batch_size: int, only_hash: bool) -> Tuple[int, float, int]:
    """
    Stream rows using a server-side cursor, compute rolling checksum and time it.
    Returns (row_count, elapsed_seconds, checksum64)
    """
    cols = get_columns(conn, schema, table)
    rowhash_expr = make_rowhash_sql(cols)

    select_list = rowhash_expr + (" " if only_hash else ", " + ", ".join(psql_ident(c) for c in cols))
    order_cols = get_primary_key(conn, schema, table) or cols  # fall back to all cols for stable order
    order_by = ", ".join(psql_ident(c) for c in order_cols)

    # Named cursor => server-side streaming
    cur_name = f"csr_{schema}_{table}_{int(time.time()*1000)}"
    cur = conn.cursor(name=cur_name, cursor_factory=psycopg2.extras.DictCursor)
    cur.itersize = batch_size

    cur.execute(f'SET LOCAL work_mem = %s', ('128MB',))  # helps ORDER BY if needed
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
            # r[0] is md5 hex string -> fold into uint64 rolling checksum (simple, fast)
            h = int(r[0], 16)
            checksum64 ^= (h & ((1<<64)-1))
            rows += 1
    elapsed = time.perf_counter() - start
    cur.close()
    return rows, elapsed, checksum64

def sql_checksum(conn, schema: str, table: str) -> Tuple[int, int]:
    """
    Single-scan SQL checksum: SUM of hashtextextended of concatenated values.
    Fast and memory-friendly. Returns (row_count, sum_hash64).
    """
    cols = get_columns(conn, schema, table)
    rowconcat = "concat_ws('||', " + ", ".join(f"COALESCE({psql_cast(c)}, '')" for c in cols) + ")"
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
    parser.add_argument("--tables", nargs="+", default=["gastnr", "genstat", "res_line", "reservation"])
    parser.add_argument("--batch-size", type=int, default=5000, help="Fetchmany batch size for streaming")
    parser.add_argument("--mode", choices=["time-loop", "checksum", "both"], default="both")
    parser.add_argument("--only-hash", action="store_true", help="When timing, fetch only the per-row hash (less network I/O)")
    args = parser.parse_args()

    try:
        conn = psycopg2.connect(args.dsn)
        conn.autocommit = False  # so SET LOCAL works

        # Print header
        print(f"Schemas: {args.schema1} vs {args.schema2}")
        print(f"Tables: {', '.join(args.tables)}")
        print(f"Mode: {args.mode} | batch={args.batch_size} | only_hash={args.only_hash}")
        print()

        for tbl in args.tables:
            print(f"=== {tbl} ===")
            if args.mode in ("time-loop", "both"):
                # schema1
                with conn:
                    rows1, t1, c1 = time_loop(conn, args.schema1, tbl, args.batch_size, args.only_hash)
                # schema2
                with conn:
                    rows2, t2, c2 = time_loop(conn, args.schema2, tbl, args.batch_size, args.only_hash)

                if rows1 != rows2:
                    note = " (DIFF rowcount!)"
                else:
                    note = ""
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
