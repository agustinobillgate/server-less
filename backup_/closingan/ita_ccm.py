import json
import psycopg2
from datetime import date, timedelta
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
HOTEL_SCHEMA = args.schema or config.get("HOTEL_SCHEMA")

if not DB_NAME or not HOTEL_SCHEMA:
    print("❌ DB_NAME dan HOTEL_SCHEMA wajib diisi di config.json atau lewat argumen --schema")
    sys.exit(1)

# ======================================================
# 3️⃣ KONEKSI KE DATABASE
# ======================================================
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
    print(f"❌ Gagal konek ke database: {e}")
    sys.exit(1)

# ======================================================
# 4️⃣ BACA CURRENT DAN LAST CLOSING PERIOD
# ======================================================
print("==============================================")
print(f" CANCEL CLOSE MONTH - SCHEMA: {HOTEL_SCHEMA} ")
print("==============================================")

cur.execute("""
    SELECT paramnr, fdate
    FROM htparam
    WHERE paramnr IN (597, 558)
""")
rows = cur.fetchall()
if len(rows) < 2:
    print("❌ Data paramnr 597 dan 558 tidak ditemukan di htparam.")
    cur.close()
    conn.close()
    sys.exit(1)

htparam = {row[0]: row[1] for row in rows}
current_period = htparam[597]
last_period = htparam[558]

print(f"Current Closing Period : {current_period}")
print(f"Last Closing Period    : {last_period}")
from_date = last_period + timedelta(days=1)
to_date = current_period
print(f"\nPeriode aktif: {from_date} s/d {to_date}")
print("==============================================")
#---------------------
param_597 = current_period
first_day_this_month = param_597.replace(day=1)
end_date_lastmonth = first_day_this_month - timedelta(days=1)
beg_date_lastmonth = end_date_lastmonth.replace(day=1)

# Assign to your variables
from_date1 = beg_date_lastmonth
to_date1 = end_date_lastmonth

# print("From Date (start of last month):", from_date1)
# print("To Date   (end of last month):  ", to_date1)


#---------------------
from_date = beg_date_lastmonth
to_date = end_date_lastmonth
print(f"\nCancel ke Periode: {from_date} s/d {to_date}")


# ======================================================
# 5️⃣ KONFIRMASI USER
# ======================================================
confirm = input("\nApakah Anda ingin membatalkan Close Month? (y/n): ").strip().lower()
if confirm not in ["y", "yes"]:
    print("\n❌ Operasi dibatalkan.")
    cur.close()
    conn.close()
    sys.exit(0)

print("\n⏳ Memproses pembatalan...")

# ======================================================
# 6️⃣ EKSEKUSI UPDATE SESUAI LOGIKA OE
# ======================================================
try:
    # Update gl_jouhdr (set activeflag=0, batch=FALSE)
    cur.execute(f"""
        UPDATE {HOTEL_SCHEMA}.gl_jouhdr
        SET activeflag = 0, batch = FALSE
        WHERE datum BETWEEN %s AND %s
    """, (from_date, to_date))

    # Update gl_journal (activeflag=0) untuk jnr terkait
    cur.execute(f"""
        UPDATE {HOTEL_SCHEMA}.gl_journal
        SET activeflag = 0
        WHERE jnr IN (
            SELECT jnr FROM {HOTEL_SCHEMA}.gl_jouhdr
            WHERE datum BETWEEN %s AND %s
        )
    """, (from_date, to_date))

    # Update htparam:
    # - Current Closing tetap sama (to_date)
    # - Last Closing = from_date - 1
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
    sys.exit(1)

# ======================================================
# 7️⃣ TAMPILKAN HASIL AKHIR
# ======================================================
cur.execute("""
    SELECT paramnr, fdate FROM htparam WHERE paramnr IN (597, 558)
""")
for paramnr, fdate in cur.fetchall():
    label = "Current Closing" if paramnr == 597 else "Last Closing"
    print(f"{label} Period: {fdate}")

cur.close()
conn.close()
print("\nSelesai ✅")
