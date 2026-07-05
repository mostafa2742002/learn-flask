from flask import Blueprint, render_template, request, redirect, url_for, flash

from user_service import register_user


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register")
def register_form():
    return render_template("register.html")


@auth_bp.route("/register", methods=["POST"])
def register_route():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    user, message = register_user(name, email, password)

    flash(message)

    if user is None:
        return render_template("register.html")

    return redirect(url_for("tickets.home"))