import psycopg2
import json
from dotenv import load_dotenv
import os

# === Load konfigurasi koneksi dari .env ===
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "hotel_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# === Fungsi utama ===
def send_json_to_db(json_file_path):
    # Baca file JSON
    with open(json_file_path, "r") as f:
        data = json.load(f)

    print(f"📦 Membaca file {json_file_path}...")
    print(json.dumps(data, indent=2))

    # Koneksi ke PostgreSQL
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    try:
        # Insert JSON ke tabel log_message
        cur.execute(
            """
            INSERT INTO log_message (raw_data)
            VALUES (%s)
            RETURNING id;
            """,
            [json.dumps(data)]  # PostgreSQL akan otomatis parse JSON string
        )

        inserted_id = cur.fetchone()[0]
        conn.commit()
        print(f"✅ Data JSON berhasil dikirim ke DB. ID = {inserted_id}")

    except Exception as e:
        conn.rollback()
        print(f"⚠️ Gagal mengirim data ke DB: {e}")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    send_json_to_db("push_data.json")
