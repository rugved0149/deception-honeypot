# app.py
import os
from flask import Flask

app = Flask(__name__)

# 🔐 REQUIRED for sessions (authentication will NOT work without this)
app.config["SECRET_KEY"] = "super_secret_demo_key_2026"

# Import blueprints AFTER app is created
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)