from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint("auth", __name__)

# Hardcoded credentials (Demo Only)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "secure123"


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard.dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("auth.login"))