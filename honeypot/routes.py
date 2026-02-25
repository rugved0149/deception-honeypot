from flask import Blueprint, jsonify, render_template, request

from utils.request_utils import (
    extract_request_data,
    classify_attack,
    is_bot_like
)
from utils.geoip_utils import lookup_country

from honeypot.logger import log_honeypot_hit
from honeypot.analyzer import analyze_honeypot_hit
from core.risk_engine import risk_engine

honeypot_bp = Blueprint("honeypot", __name__)

@honeypot_bp.route("/admin", methods=["GET", "POST"])
def fake_admin_login():
    data = extract_request_data()
    ip = data.get("ip")

    data["attack_type"] = classify_attack(data["path"], data["method"])
    data["bot_like"] = is_bot_like(data.get("user_agent"))
    data["country"] = lookup_country(ip)

    if request.method == "POST":
        data["submitted_username"] = request.form.get("username")
        data["submitted_password"] = request.form.get("password")

    log_honeypot_hit(data)
    analyze_honeypot_hit(ip)

    # Always respond normally
    if request.method == "POST":
        return jsonify({
            "message": "Invalid credentials"
        })

    return render_template("admin_login.html")

@honeypot_bp.route("/.env", methods=["GET"])
@honeypot_bp.route("/config", methods=["GET"])
def honeypot_files():
    data = extract_request_data()
    ip = data.get("ip")

    data["attack_type"] = classify_attack(data["path"], data["method"])
    data["bot_like"] = is_bot_like(data.get("user_agent"))
    data["country"] = lookup_country(ip)

    log_honeypot_hit(data)
    analyze_honeypot_hit(ip)

    # Fake .env content (realistic looking)
    fake_env = """APP_ENV=production
APP_DEBUG=false
APP_KEY=base64:ZHVtbXlLZXlGb3JEZW1v
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=prod_db
DB_USERNAME=root
DB_PASSWORD=SuperSecretPassword123
MAIL_HOST=smtp.mailserver.com
MAIL_PORT=587
"""

    return fake_env, 200, {
        "Content-Type": "text/plain"
    }

@honeypot_bp.route("/backup.zip")
@honeypot_bp.route("/db_dump.sql")
def fake_downloads():
    data = extract_request_data()
    ip = data.get("ip")

    data["attack_type"] = classify_attack(data["path"], data["method"])
    data["bot_like"] = is_bot_like(data.get("user_agent"))
    data["country"] = lookup_country(ip)

    log_honeypot_hit(data)
    analyze_honeypot_hit(ip)

    fake_content = "ACCESS DENIED\nTHIS INCIDENT IS LOGGED"

    return fake_content, 200, {
        "Content-Type": "application/octet-stream",
        "Content-Disposition": "attachment; filename=fake_backup.zip"
    }
