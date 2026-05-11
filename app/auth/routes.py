from flask import Blueprint, flash, make_response, redirect, render_template, url_for
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from sqlalchemy import or_

from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please sign in.", "success")
        return redirect(url_for("auth.login"))

    if form.is_submitted() and form.errors:
        flash("Please correct the errors below.", "error")

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        identifier = form.username.data.strip()
        user = User.query.filter(
            or_(
                User.username == identifier,
                User.email == identifier.lower(),
            )
        ).first()

        if user and user.check_password(form.password.data):
            access_token = create_access_token(identity=str(user.id))
            response = make_response(redirect(url_for("game.select_game")))
            set_access_cookies(response, access_token)
            flash("Login successful. Welcome back!", "success")
            return response

        flash("Invalid credentials.", "error")

    elif form.is_submitted() and form.errors:
        flash("Please correct the errors below.", "error")

    return render_template("auth/login.html", form=form)


@auth_bp.get("/logout")
def logout():
    response = make_response(redirect(url_for("index")))
    unset_jwt_cookies(response)
    flash("You have been signed out.", "success")
    return response
