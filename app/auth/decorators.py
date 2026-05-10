from functools import wraps

from flask import abort, flash, g, redirect, url_for
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException

from app import db
from app.models import User


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=["cookies"])
            identity = get_jwt_identity()
            current_user = db.session.get(User, int(identity))
            if current_user is None:
                raise JWTExtendedException("Authenticated user no longer exists.")
        except (JWTExtendedException, ValueError, TypeError):
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))

        g.current_user = current_user
        return view_func(*args, **kwargs)

    return wrapped_view


def admin_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not g.current_user.is_admin:
            abort(403)
        return view_func(*args, **kwargs)

    return wrapped_view
