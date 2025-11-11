import psycopg2
import select
import json


conn = psycopg2.connect(
    dbname="qctest",
    user="postgres",
    password="DevPostgreSQL#2024",
    host="psql.staging.e1-vhp.com",  # contoh: "192.168.1.10" atau "db.hotel.local"
    port="5432"
)

conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
cur.execute("LISTEN error_channel;")
print("✅ Listening for notifications on channel 'error_channel'...")

try:
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            data = json.loads(notify.payload)
            print(f"\n🔔 Error notification received:")
            print(f"   Endpoint  : {data['endpoint']}")
            print(f"   Time      : {data['time']}")
            print(f"   Message   : {data['error_message']}")
except KeyboardInterrupt:
    print("\n👋 Listener stopped.")
finally:
    cur.close()
    conn.close()

"""
import psycopg2
import select
import json
import subprocess
import sys

# === Koneksi ke PostgreSQL (Server A) ===
conn = psycopg2.connect(
    dbname="hotel_db",
    user="postgres",
    password="1234",
    host="192.168.1.10",  # ganti sesuai host DB server A
    port="5432"
)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.execute("LISTEN error_channel;")
print("✅ Listening for notifications on channel 'error_channel'...")

# === Fungsi jalankan script tanpa menunggu ===
def run_external_script(action: str):

    cmd = ["python3", "run_sql.py", "--task", action]
    try:
        # stdout dan stderr diarahkan ke /dev/null supaya tidak blocking
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"🚀 Started background process for action: {action}")
    except Exception as e:
        print(f"⚠️ Gagal menjalankan subprocess untuk {action}: {e}", file=sys.stderr)

try:
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            continue
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            try:
                data = json.loads(notify.payload)
                print(f"\n🔔 Notification received:")
                print(f"   Endpoint  : {data.get('endpoint')}")
                print(f"   Time      : {data.get('time')}")
                print(f"   Message   : {data.get('error_message')}")
                
                # Ambil "action" dari payload
                action = data.get("action", "").lower()
                if action:
                    run_external_script(action)
                else:
                    print("ℹ️  Tidak ada 'action' di payload.")
            except Exception as e:
                print(f"⚠️ Error decoding payload: {e}\nRaw payload: {notify.payload}")

except KeyboardInterrupt:
    print("\n👋 Listener stopped.")
finally:
    cur.close()
    conn.close()

"""