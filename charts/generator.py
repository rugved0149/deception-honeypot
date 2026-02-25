import matplotlib
from flask import Flask
import sqlite3
import matplotlib.pyplot as plt
from utils.paths import DB_PATH

DB_PATH = "storage/honeypot_logs.db"

matplotlib.use("Agg")

app = Flask(__name__)
app.secret_key = "super_secret_demo_key_2026"

def generate_top_paths_chart():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT path, COUNT(*) as hits
        FROM honeypot_hits
        GROUP BY path
        ORDER BY hits DESC
        LIMIT 5
    """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        return

    paths, hits = zip(*data)

    plt.figure()
    plt.bar(paths, hits)
    plt.title("Top Targeted Endpoints")
    plt.xlabel("Endpoint")
    plt.ylabel("Hits")
    plt.tight_layout()
    plt.savefig("static/top_paths.png")
    plt.close()


def generate_top_ips_chart():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ip, COUNT(*) as hits
        FROM honeypot_hits
        GROUP BY ip
        ORDER BY hits DESC
        LIMIT 5
    """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        return

    ips, hits = zip(*data)

    plt.figure()
    plt.bar(ips, hits)
    plt.title("Top Attacking IPs")
    plt.xlabel("IP Address")
    plt.ylabel("Hits")
    plt.tight_layout()
    plt.savefig("static/top_ips.png")
    plt.close()
