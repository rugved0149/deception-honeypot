# app.py

import os
from flask import Flask
from storage.init_db import init_db
from utils.paths import DB_PATH

# Create Flask app
app = Flask(__name__)

# Secret key for sessions
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "super_secret_demo_key_2026"
)

# --- Initialize database at startup ---
print(f"[STARTUP] Using database at: {DB_PATH}")
init_db()
print("[STARTUP] Database initialization complete")

# --- Import blueprints AFTER app + DB setup ---
from auth.routes import auth_bp
from honeypot.routes import honeypot_bp
from dashboard.views import dashboard_bp
from export.views import export_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(honeypot_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(export_bp)


@app.route("/")
def home():
    return "App is running normally"


# Only used when running locally
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)