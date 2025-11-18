# db.py
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}


def connect_to_schema(schema_name: str):
    if not schema_name:
        raise ValueError("schema_name harus diisi")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # SET search_path ke schema yang dipilih
    cur.execute(f'SET search_path TO "{schema_name}"')

    return conn, cur
