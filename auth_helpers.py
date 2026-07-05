from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Please login first")
            return redirect(url_for("auth.login_form"))

        return route_function(*args, **kwargs)

    return wrapper