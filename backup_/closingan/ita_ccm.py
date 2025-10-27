import json
import psycopg2
from datetime import timedelta
from pathlib import Path
import sys
import argparse

# ======================================================
# 1️⃣ PARSE ARGUMEN CLI
# ======================================================
parser = argparse.ArgumentParser(description="Cancel Close Month (Text-based)")
parser.add_argument("--schema", type=str, help="Override hotel schema (optional)")
args = parser.parse_args()

# ======================================================
# 2️⃣ BACA FILE KONFIGURASI JSON
# ======================================================
config_path = Path(__file__).parent / "config.json"

if not config_path.exists():
    print("❌ File config.json tidak ditemukan di folder saat ini.")
    sys.exit(1)

try:
    with open(config_path, "r") as f:
        config = json.load(f)
except Exception as e:
    print(f"❌ Gagal membaca config.json: {e}")
    sys.exit(1)

DB_HOST = config.get("DB_HOST", "localhost")
DB_NAME = config.get("DB_NAME")
DB_USER = config.get("DB_USER", "postgres")
DB_PASSWORD = config.get("DB_PASSWORD", "")
DB_PORT = config.get("DB_PORT", 5432)

if not DB_NAME:
    print("❌ DB_NAME wajib diisi di config.json")
    sys.exit(1)

# ======================================================
# 3️⃣ FUNGSI PILIH SCHEMA
# ======================================================
def pilih_schema():
    try:
        conn_temp = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur_temp = conn_temp.cursor()
    except Exception as e:
        print(f"❌ Gagal konek ke database: {e}")
        sys.exit(1)

    if args.schema:
        return args.schema

    # Dapatkan semua schema hotel
    cur_temp.execute("""
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'public', 'deepseek')
          AND schema_name NOT LIKE 'pg_%'
        ORDER BY schema_name
    """)
    schemas = [row[0] for row in cur_temp.fetchall()]

    if not schemas:
        print("❌ Tidak ada schema hotel ditemukan.")
        cur_temp.close()
        conn_temp.close()
        sys.exit(1)

    print("\nDaftar hotel schema beserta param 597 dan 558:")
    print("--------------------------------------------------------------")

    for i, s in enumerate(schemas, start=1):
        try:
            cur_temp.execute(f"""
                SELECT paramnr, fdate
                FROM {s}.htparam
                WHERE paramnr IN (597, 558)
                ORDER BY paramnr
            """)
            rows = cur_temp.fetchall()
            if len(rows) == 2:
                p597 = rows[1][1] if rows[1][0] == 597 else rows[0][1]
                p558 = rows[0][1] if rows[0][0] == 558 else rows[1][1]
                print(f"{i:>2}. {s:<20} | 597: {p597} | 558: {p558}")
            else:
                print(f"{i:>2}. {s:<20} | ⚠️ param 597/558 tidak lengkap")
        except Exception as e:
            print(f"{i:>2}. {s:<20} | ❌ Gagal baca htparam: {e}")

    cur_temp.close()
    conn_temp.close()

    choice = input("\nMasukkan nomor schema yang ingin digunakan: ").strip()
    try:
        return schemas[int(choice) - 1]
    except Exception:
        print("❌ Pilihan tidak valid.")
        return pilih_schema()

# ======================================================
# 4️⃣ LOOP UTAMA - PILIH SCHEMA DAN PROSES
# ======================================================
while True:
    HOTEL_SCHEMA = pilih_schema()
    print(f"\n✅ Schema yang digunakan: {HOTEL_SCHEMA}")

    # ------------------------------------------------------
    # 5️⃣ KONEKSI KE DATABASE UTAMA
    # ------------------------------------------------------
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            options=f"-c search_path={HOTEL_SCHEMA}"
        )
        cur = conn.cursor()
    except Exception as e:
        print(f"❌ Gagal konek ke database schema {HOTEL_SCHEMA}: {e}")
        continue  # kembali ke menu schema

    # ------------------------------------------------------
    # 6️⃣ BACA CURRENT DAN LAST CLOSING PERIOD
    # ------------------------------------------------------
    print("==============================================")
    print(f" CANCEL CLOSE MONTH - SCHEMA: {HOTEL_SCHEMA} ")
    print("==============================================")

    try:
        cur.execute("""
            SELECT paramnr, fdate
            FROM htparam
            WHERE paramnr IN (597, 558)
        """)
        rows = cur.fetchall()
    except Exception as e:
        print(f"❌ Gagal membaca htparam: {e}")
        cur.close()
        conn.close()
        continue

    if len(rows) < 2:
        print("❌ Data paramnr 597 dan 558 tidak ditemukan di htparam.")
        cur.close()
        conn.close()
        continue

    htparam = {row[0]: row[1] for row in rows}
    current_period = htparam[597]
    last_period = htparam[558]

    print(f"Current Closing Period : {current_period}")
    print(f"Last Closing Period    : {last_period}")
    from_date = last_period + timedelta(days=1)
    to_date = current_period
    print(f"\nPeriode aktif: {from_date} s/d {to_date}")
    print("==============================================")

    # Hitung periode bulan sebelumnya
    param_597 = current_period
    first_day_this_month = param_597.replace(day=1)
    end_date_lastmonth = first_day_this_month - timedelta(days=1)
    beg_date_lastmonth = end_date_lastmonth.replace(day=1)

    from_date = beg_date_lastmonth
    to_date = end_date_lastmonth
    print(f"\nCancel ke Periode: {from_date} s/d {to_date}")

    # ------------------------------------------------------
    # 7️⃣ KONFIRMASI USER
    # ------------------------------------------------------
    confirm = input("\nApakah Anda ingin membatalkan Close Month? (y/n): ").strip().lower()
    if confirm not in ["y", "yes"]:
        print("\n🔁 Kembali ke menu pilihan schema...\n")
        cur.close()
        conn.close()
        continue  # kembali ke menu schema

    print("\n⏳ Memproses pembatalan...")

    # ------------------------------------------------------
    # 8️⃣ EKSEKUSI UPDATE SESUAI LOGIKA OE
    # ------------------------------------------------------
    try:
        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.gl_jouhdr
            SET activeflag = 0, batch = FALSE
            WHERE datum BETWEEN %s AND %s
        """, (from_date, to_date))

        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.gl_journal
            SET activeflag = 0
            WHERE jnr IN (
                SELECT jnr FROM {HOTEL_SCHEMA}.gl_jouhdr
                WHERE datum BETWEEN %s AND %s
            )
        """, (from_date, to_date))

        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.htparam
            SET fdate = %s WHERE paramnr = 597
        """, (to_date,))

        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.htparam
            SET fdate = %s WHERE paramnr = 558
        """, (from_date - timedelta(days=1),))

        conn.commit()
        print("✅ Pembatalan Close Month selesai.\n")

    except Exception as e:
        conn.rollback()
        print(f"❌ Terjadi error saat update: {e}")
        cur.close()
        conn.close()
        continue

    # ------------------------------------------------------
    # 9️⃣ TAMPILKAN HASIL AKHIR
    # ------------------------------------------------------
    cur.execute("""
        SELECT paramnr, fdate FROM htparam WHERE paramnr IN (597, 558)
    """)
    for paramnr, fdate in cur.fetchall():
        label = "Current Closing" if paramnr == 597 else "Last Closing"
        print(f"{label} Period: {fdate}")

    cur.close()
    conn.close()

    # ------------------------------------------------------
    # 🔁 Tanya apakah mau kembali ke menu schema
    # ------------------------------------------------------
    again = input("\nApakah ingin kembali ke menu pilihan schema? (y/n): ").strip().lower()
    if again in ["y", "yes"]:
        print("\n🔁 Kembali ke menu pilihan schema...\n")
        continue
    else:
        print("\n✅ Selesai. Keluar dari program.")
        break
