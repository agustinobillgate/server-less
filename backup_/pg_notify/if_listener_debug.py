import psycopg2
import select
import json
import time
import os
from dotenv import load_dotenv

def start_listener():
    # === Load environment variables ===
    load_dotenv()

    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    channel = os.getenv("CHANNEL_NAME", "notify_channel")

    while True:
        try:
            print(f"🔌 Connecting to PostgreSQL ({host}:{port})...")
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            cur.execute(f"LISTEN {channel};")
            print(f"✅ Listening on channel '{channel}'...\n")

            # Loop utama
            while True:
                if select.select([conn], [], [], 5) == ([], [], []):
                    continue
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    try:
                        data = json.loads(notify.payload)
                        print("🔔 Received notification:")
                        print(json.dumps(data, indent=4))
                        print("-" * 60)
                    except json.JSONDecodeError:
                        print(f"⚠️ Received raw payload: {notify.payload}")
                        print("-" * 60)

        except psycopg2.OperationalError as e:
            print(f"⚠️ Connection lost: {e}")
            print("🔁 Reconnecting in 5 seconds...\n")
            time.sleep(5)
            continue

        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            time.sleep(5)
            continue

        finally:
            try:
                if conn:
                    conn.close()
            except:
                pass

if __name__ == "__main__":
    start_listener()
