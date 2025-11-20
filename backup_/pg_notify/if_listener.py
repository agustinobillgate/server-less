import psycopg2, select, json, subprocess, time, os
from dotenv import load_dotenv

def run_task(key_value, recid: int):
    """
    Jalankan script eksternal secara async (tidak menunggu selesai).
    key_value: nilai dari kolom 'key' di tabel interface (int atau string)
    recid: id record yang diproses
    """
    # Mapping script berdasarkan nilai key
    map_scripts = {
        "1": "push_all.py",      # key=1 → jalankan push_all.py
        "0": "push_partial.py"   # key selain 1 → jalankan push_partial.py
    }

    # Normalisasi tipe (karena bisa int dari JSON)
    key_str = str(key_value).strip()
    script = map_scripts.get(key_str, "push_partial.py")

    # Jalankan subprocess tanpa menunggu selesai
    cmd = ["python3", script, str(recid)]
    try:
        # subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"🚀 Started subprocess: {script} (recid={recid}, key={key_str})")
    except Exception as e:
        print(f"⚠️ Gagal menjalankan {script} untuk recid={recid}: {e}")

def start_listener():
    load_dotenv()

    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    channel = os.getenv("CHANNEL_NAME", "notify_channel")
    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute("LISTEN notify_channel;")
            print("✅ Listening on 'notify_channel'...")

            while True:
                if select.select([conn], [], [], 5) == ([], [], []):
                    continue
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    data = json.loads(notify.payload)

                    if data.get("type") == "interface":
                        push_all = data.get("push_all", False)
                        recid = data.get("recid", 0)
                        print(f"🔔 Event on {data['table']} (key={data['key']}, Action={data['action']})")
                        run_task(data.get("key"), recid)

        except Exception as e:
            print(f"⚠️ Connection error: {e}, reconnecting in 5s...")
            time.sleep(5)

if __name__ == "__main__":
    start_listener()
