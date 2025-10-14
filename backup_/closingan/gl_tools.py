import json
import psycopg2
from datetime import date, timedelta
from pathlib import Path
import sys
import argparse

# ======================================================
# 1️⃣ LOAD CONFIGURATION
# ======================================================
config_path = Path(__file__).parent / "config.json"
if not config_path.exists():
    print("❌ File config.json tidak ditemukan.")
    sys.exit(1)

with open(config_path, "r") as f:
    config = json.load(f)

DB_HOST = config.get("DB_HOST", "localhost")
DB_NAME = config.get("DB_NAME")
DB_USER = config.get("DB_USER", "postgres")
DB_PASSWORD = config.get("DB_PASSWORD", "")
DB_PORT = config.get("DB_PORT", 5432)
HOTEL_SCHEMA = config.get("HOTEL_SCHEMA")

parser = argparse.ArgumentParser(description="GL Tools (Reopen Month/Year/Budget)")
parser.add_argument("--schema", type=str, help="Override schema name")
args = parser.parse_args()
if args.schema:
    HOTEL_SCHEMA = args.schema

if not DB_NAME or not HOTEL_SCHEMA:
    print("❌ DB_NAME dan HOTEL_SCHEMA wajib diisi dalam config.json.")
    sys.exit(1)

# ======================================================
# 2️⃣ CONNECT TO POSTGRESQL
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
# 3️⃣ FETCH PERIOD PARAMETERS
# ======================================================
def get_htparams():
    """Ambil semua periode (558, 597, 598, 795) dari htparam"""
    cur.execute("""
        SELECT paramnr, fdate
        FROM htparam
        WHERE paramnr IN (558, 597, 598, 795)
    """)
    params = dict(cur.fetchall())
    return params.get(597), params.get(558), params.get(795), params.get(598)

cacm, lacm, lacy, nacm = get_htparams()

print("==============================================")
print(f" G/L TOOLS - SCHEMA: {HOTEL_SCHEMA} ")
print("==============================================")
print(f"Current Closing Period : {cacm}")
print(f"Last Closing Period    : {lacm}")
print(f"Next Closing Period    : {nacm}")
print(f"Last Closing Year      : {lacy}")
print("==============================================")
print("1. Re-Open Closed Month")
print("2. Re-Open Closed Year")
print("3. Restore CoA & Budget")
print("4. Info Table yang berubah (Cancel Close Month)")
print("==============================================")

try:
    choice = int(input("Pilih menu (1/2/3/4): ").strip())
except ValueError:
    print("❌ Pilihan tidak valid.")
    sys.exit(1)

# ======================================================
# 4️⃣ RE-OPEN CLOSED MONTH
# ======================================================
def reopen_month(cacm, lacm, lacy):
    print(f"\nCurrent Closing Month : {cacm}")
    print(f"Last Closing Month    : {lacm}")
    print(f"Last Closing Year     : {lacy}")

    confirm = input(f"\nApakah Anda yakin ingin Re-Open Closed Month {lacm}? (y/n): ").lower()
    if confirm not in ["y", "yes"]:
        print("❌ Operasi dibatalkan.")
        return

    if not (lacm and lacy and cacm):
        print("❌ Parameter periode tidak lengkap di htparam.")
        return

    if lacm <= lacy or cacm <= lacm:
        print("❌ Urutan periode tidak valid (lacm <= lacy atau cacm <= lacm).")
        return

    fdate = date(lacm.year, lacm.month, 1)
    tdate = lacm
    print(f"⏳ Membuka periode {fdate} s/d {tdate}...")

    try:
        # Update gl_jouhdr
        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.gl_jouhdr
            SET activeflag = 0, batch = CASE WHEN jtype=0 THEN FALSE ELSE TRUE END
            WHERE datum BETWEEN %s AND %s
        """, (fdate, tdate))

        # Update gl_journal
        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.gl_journal
            SET activeflag = 0
            WHERE jnr IN (
                SELECT jnr FROM {HOTEL_SCHEMA}.gl_jouhdr
                WHERE datum BETWEEN %s AND %s
            )
        """, (fdate, tdate))

        # Reset actual bulan terkait
        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.gl_acct
            SET actual[EXTRACT(MONTH FROM %s)::int] = 0
        """, (lacm,))

        # Update htparam periode
        cur.execute(f"UPDATE {HOTEL_SCHEMA}.htparam SET fdate = %s WHERE paramnr = 597", (tdate,))
        cur.execute(f"UPDATE {HOTEL_SCHEMA}.htparam SET fdate = %s WHERE paramnr = 558", (fdate - timedelta(days=1),))

        conn.commit()
        print("✅ Re-Open Closed Month selesai.")
        print(f"   Current Closing Period: {tdate}")
        print(f"   Last Closing Period   : {fdate - timedelta(days=1)}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error saat Re-Open Closed Month: {e}")

# ======================================================
# 5️⃣ RE-OPEN CLOSED YEAR (simplified)
# ======================================================
def reopen_year(cacm, lacm, lacy):
    print(f"\nCurrent Closing Year : {lacy.year}")
    confirm = input(f"Apakah Anda yakin ingin Re-Open Closed Year {lacy.year}? (y/n): ").lower()
    if confirm not in ["y", "yes"]:
        print("❌ Operasi dibatalkan.")
        return

    print("⏳ Membuka tahun berjalan... (versi sederhana)")
    try:
        # Reset seluruh actual dan budget (simulasi seperti ABL)
        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.gl_acct
            SET actual = ARRAY_FILL(0, ARRAY[12]),
                budget = ARRAY_FILL(0, ARRAY[12]),
                last_yr = ARRAY_FILL(0, ARRAY[12]),
                ly_budget = ARRAY_FILL(0, ARRAY[12])
        """)

        # Update htparam tahun
        cur.execute(f"UPDATE {HOTEL_SCHEMA}.htparam SET fdate = %s WHERE paramnr = 597", (date(lacy.year, 12, 31),))
        cur.execute(f"UPDATE {HOTEL_SCHEMA}.htparam SET fdate = %s WHERE paramnr = 558", (date(lacy.year, 11, 30),))
        cur.execute(f"UPDATE {HOTEL_SCHEMA}.htparam SET fdate = %s WHERE paramnr = 795", (date(lacy.year - 1, 12, 31),))
        conn.commit()
        print("✅ Re-Open Closed Year selesai.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error saat Re-Open Year: {e}")

# ======================================================
# 6️⃣ RESTORE COA & BUDGET
# ======================================================
def restore_budget(lacy):
    confirm = input(f"\nApakah Anda ingin Restore CoA Budget tahun {lacy.year + 1}? (y/n): ").lower()
    if confirm not in ["y", "yes"]:
        print("❌ Operasi dibatalkan.")
        return

    backup_year = lacy.year + 1001
    print(f"⏳ Mengembalikan budget dari gl_accthis YEAR={backup_year}...")

    try:
        # Kosongkan budget gl_acct
        cur.execute(f"UPDATE {HOTEL_SCHEMA}.gl_acct SET budget = ARRAY_FILL(0, ARRAY[12])")

        # Copy dari gl_accthis
        cur.execute(f"""
            UPDATE {HOTEL_SCHEMA}.gl_acct AS a
            SET budget = b.budget
            FROM {HOTEL_SCHEMA}.gl_accthis AS b
            WHERE a.fibukonto = b.fibukonto
            AND b.year = %s
        """, (backup_year,))

        conn.commit()
        print("✅ Restore CoA Budget selesai.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Error saat Restore CoA Budget: {e}")

# ======================================================
# 7️⃣ INFO TABLE YANG BERUBAH
# ======================================================
def info_table():
    print("\n🧾 Table yang berubah saat Cancel Close Month:")
    print("==============================================")
    print("1. gl_jouhdr   → activeflag, batch")
    print("2. gl_journal  → activeflag")
    print("3. gl_acct     → actual[cMonth]")
    print("4. htparam     → fdate (paramnr 597, 558)")
    print("----------------------------------------------")
    print("Total: 4 tabel yang diperbarui saat Re-Open Month.")
    print("Tidak ada perubahan pada budget, last-year, atau ly-budget.")
    print("==============================================\n")

# ======================================================
# 8️⃣ EXECUTE MENU
# ======================================================
if choice == 1:
    reopen_month(cacm, lacm, lacy)
elif choice == 2:
    reopen_year(cacm, lacm, lacy)
elif choice == 3:
    restore_budget(lacy)
elif choice == 4:
    info_table()
else:
    print("❌ Pilihan tidak valid.")

cur.close()
conn.close()
print("\nSelesai ✅")
