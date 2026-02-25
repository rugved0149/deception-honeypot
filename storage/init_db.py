import sqlite3
from utils.paths import DB_PATH

conn = sqlite3.connect("storage/honeypot_logs.db")
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

print("Database initialized")
