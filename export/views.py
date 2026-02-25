import sqlite3
import csv
import json
from flask import Blueprint, Response
from utils.paths import DB_PATH
from flask import session, redirect, url_for

export_bp = Blueprint("export", __name__)
DB_PATH = "storage/honeypot_logs.db"


@export_bp.route("/export/csv")
def export_csv():
    if not session.get("admin_logged_in"):
        return redirect(url_for("auth.login"))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM honeypot_hits")
    rows = cursor.fetchall()

    headers = [description[0] for description in cursor.description]
    conn.close()

    def generate():
        yield ",".join(headers) + "\n"
        for row in rows:
            yield ",".join([str(item) for item in row]) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=honeypot_logs.csv"
        }
    )


@export_bp.route("/export/json")
def export_json():
    if not session.get("admin_logged_in"):
        return redirect(url_for("auth.login"))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM honeypot_hits")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]

    conn.close()

    data = [dict(zip(headers, row)) for row in rows]

    return Response(
        json.dumps(data, indent=2),
        mimetype="application/json",
        headers={
            "Content-Disposition": "attachment; filename=honeypot_logs.json"
        }
    )
