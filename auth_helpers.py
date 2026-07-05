from functools import wraps
import secrets

from flask import session, redirect, url_for, flash, request, abort


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please login first", "warning")
            return redirect(url_for("auth.login_form"))

        return route_function(*args, **kwargs)

    return wrapper


def generate_csrf_token():
    if session.get("csrf_token") is None:
        session["csrf_token"] = secrets.token_hex(32)

    return session["csrf_token"]


def csrf_protect(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        session_token = session.get("csrf_token")
        form_token = request.form.get("csrf_token")

        if session_token is None or form_token is None or session_token != form_token:
            abort(403)

        return route_function(*args, **kwargs)

    return wrapper