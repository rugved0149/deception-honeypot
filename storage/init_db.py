import os
import sqlite3
from utils.paths import DB_PATH, STORAGE_DIR

def init_db():
    os.makedirs(STORAGE_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS honeypot_hits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            method TEXT,
            path TEXT,
            user_agent TEXT,
            payload TEXT
        )
    """)

    conn.commit()
    conn.close()

    print(f"Database initialized at: {DB_PATH}")