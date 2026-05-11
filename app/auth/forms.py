import re

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=80),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(check_deliverability=False),
            Length(max=120),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=128),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Create Account")

    def validate_username(self, field) -> None:
        existing_user = User.query.filter_by(username=field.data.strip()).first()
        if existing_user:
            raise ValidationError("That username is already taken.")

    def validate_email(self, field) -> None:
        existing_user = User.query.filter_by(email=field.data.strip().lower()).first()
        if existing_user:
            raise ValidationError("That email is already registered.")

    def validate_password(self, field) -> None:
        password = field.data or ""
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must include at least one uppercase letter.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must include at least one number.")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError("Password must include at least one special character.")


class LoginForm(FlaskForm):
    username = StringField(
        "Username or Email",
        validators=[
            DataRequired(),
            Length(min=3, max=80),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=128),
        ],
    )
    submit = SubmitField("Sign In")
