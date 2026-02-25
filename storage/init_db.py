# storage/init_db.py

import os
import sqlite3
from utils.paths import DB_PATH


def init_db():
    # Ensure storage directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

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

    print("Database initialized successfully.")