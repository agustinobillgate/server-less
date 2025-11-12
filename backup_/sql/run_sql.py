import os
import json
from sqlalchemy import create_engine, text

# === 1. Baca koneksi dari config.json ===
CONFIG_PATH = "config.json"
SQL_FOLDER = "backup_/sql"

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

db_host = config["database"]["ec2_qc"]["DB_HOST"]
db_user = config["database"]["ec2_qc"]["DB_USER"]
db_password = config["database"]["ec2_qc"]["DB_PASSWORD"]
db_port = config["database"]["ec2_qc"]["DB_PORT"]
db_name = config["database"]["ec2_qc"]["DB_NAME"]
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url)

# === Fungsi untuk menjalankan 1 file SQL ===
def run_sql_file(file_name):
    sql_path = os.path.join(SQL_FOLDER, file_name)

    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    print(f"\n🚀 Menjalankan {file_name}...\n")

    with engine.connect() as conn:
        try:
            result = conn.execute(text(sql_script))
            # Jika query menghasilkan data (SELECT), tampilkan
            if result.returns_rows:
                rows = result.fetchall()
                if rows:
                    print(f"✅ Hasil ({len(rows)} baris):\n")
                    print(" | ".join(result.keys()))
                    print("-" * 60)
                    for row in rows:
                        print(" | ".join(str(v) for v in row))
                else:
                    print("✅ Query berhasil, tetapi tidak ada hasil.")
            else:
                print("✅ Query berhasil dijalankan (non-SELECT).")
        except Exception as e:
            print("❌ Error saat menjalankan SQL:", e)

# === Loop utama ===
while True:
    sql_files = [f for f in os.listdir(SQL_FOLDER) if f.endswith(".sql")]

    if not sql_files:
        print("❌ Tidak ada file .sql di folder", SQL_FOLDER)
        break

    print("\n📄 Daftar file SQL:")
    for i, file in enumerate(sql_files, start=1):
        print(f"{i}. {file}")
    print("0. ❌ Keluar")

    # === Pilih file ===
    try:
        choice = int(input("\nPilih nomor file SQL yang akan dijalankan: "))
        if choice == 0:
            print("👋 Keluar dari program.")
            break
        selected_file = sql_files[choice - 1]
    except (ValueError, IndexError):
        print("❌ Pilihan tidak valid. Coba lagi.")
        continue

    # Jalankan file
    run_sql_file(selected_file)

    # Tanya apakah ingin lanjut
    again = input("\nIngin menjalankan file lain? (y/n): ").strip().lower()
    if again != "y":
        print("👋 Selesai. Terima kasih!")
        break
