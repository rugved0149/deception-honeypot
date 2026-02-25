# charts/generator.py

import os
import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from utils.paths import DB_PATH, BASE_DIR


def _ensure_static_folder():
    static_dir = os.path.join(BASE_DIR, "static")
    os.makedirs(static_dir, exist_ok=True)
    return static_dir


def generate_top_paths_chart():
    static_dir = _ensure_static_folder()
    output_path = os.path.join(static_dir, "top_paths.png")

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
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def generate_top_ips_chart():
    static_dir = _ensure_static_folder()
    output_path = os.path.join(static_dir, "top_ips.png")

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
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()