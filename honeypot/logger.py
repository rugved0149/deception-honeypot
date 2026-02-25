import sqlite3
import json
from datetime import datetime
from utils.paths import DB_PATH   # ← THIS IS CRITICAL

def log_honeypot_hit(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO honeypot_hits
        (timestamp, ip, method, path, user_agent, payload)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        data.get("ip"),
        data.get("method"),
        data.get("path"),
        data.get("user_agent"),
        json.dumps(data)
    ))

    conn.commit()
    conn.close()
