from functools import wraps

from flask import abort, current_app, flash, g, redirect, request, url_for
from flask_jwt_extended import decode_token, unset_jwt_cookies

from app import db
from app.models import User


def get_user_from_request_cookie() -> User | None:
    token_cookie_name = current_app.config.get(
        "JWT_ACCESS_COOKIE_NAME",
        "access_token_cookie",
    )
    encoded_token = request.cookies.get(token_cookie_name)
    if not encoded_token:
        return None

    try:
        decoded_token = decode_token(encoded_token)
        identity_claim = current_app.config.get("JWT_IDENTITY_CLAIM", "sub")
        identity = decoded_token.get(identity_claim)
        if identity is None:
            return None
        return db.session.get(User, int(identity))
    except Exception:
        return None


def _redirect_to_login():
    flash("Please log in to continue.", "error")
    response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)
    return response


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        current_user = get_user_from_request_cookie()
        if current_user is None:
            return _redirect_to_login()

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
