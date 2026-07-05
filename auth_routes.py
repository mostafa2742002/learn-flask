from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from user_service import register_user, login_user


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
        return render_template("register.html", name=name, email=email)

    return redirect(url_for("auth.login_form"))


@auth_bp.route("/login")
def login_form():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_route():
    email = request.form["email"]
    password = request.form["password"]

    user, message = login_user(email, password)

    flash(message)

    if user is None:
        return render_template("login.html", email=email)

    session["user_id"] = user.id
    session["user_name"] = user.name
    session["user_email"] = user.email

    return redirect(url_for("tickets.home"))


@auth_bp.route("/logout")
def logout_route():
    session.clear()

    flash("Logged out successfully")

    return redirect(url_for("auth.login_form"))