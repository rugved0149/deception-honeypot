import sqlite3
from flask import Blueprint, render_template
from core.risk_engine import risk_engine
from charts.generator import generate_top_paths_chart, generate_top_ips_chart
from utils.paths import DB_PATH
from flask import session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)
@dashboard_bp.route("/dashboard")

def dashboard():

    if not session.get("admin_logged_in"):
        return redirect(url_for("auth.login"))
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Total hits
    cursor.execute("SELECT COUNT(*) FROM honeypot_hits")
    total_hits = cursor.fetchone()[0]

    # Top attacking IPs
    cursor.execute("""
        SELECT ip, COUNT(*) as hits
        FROM honeypot_hits
        GROUP BY ip
        ORDER BY hits DESC
        LIMIT 5
    """)
    top_ips = cursor.fetchall()

    # Most targeted endpoints
    cursor.execute("""
        SELECT path, COUNT(*) as hits
        FROM honeypot_hits
        GROUP BY path
        ORDER BY hits DESC
        LIMIT 5
    """)
    top_paths = cursor.fetchall()

    # Recent attacks
    cursor.execute("""
        SELECT timestamp, ip, path, user_agent
        FROM honeypot_hits
        ORDER BY id DESC
        LIMIT 10
    """)
    recent_hits = cursor.fetchall()

    conn.close()

    # 🔹 Generate charts
    generate_top_paths_chart()
    generate_top_ips_chart()

    # 🔹 GET RISK DATA (THIS WAS MISSING)
    risk_data = risk_engine.get_all_risks()

    # 🔹 PASS EVERYTHING TO TEMPLATE
    return render_template(
        "dashboard.html",
        total_hits=total_hits,
        top_ips=top_ips,
        top_paths=top_paths,
        recent_hits=recent_hits,
        risk_data=risk_data   # ✅ THIS FIXES THE ERROR
    )
