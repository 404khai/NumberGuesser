import secrets
from datetime import date

import click
from flask import flash, g, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func
from werkzeug.exceptions import Forbidden

from app import db
from app.auth.decorators import admin_required
from app.models import Feedback, Game, Guess, User


@admin_required
def _admin_guard():
    return None


class SecureAdminMixin:
    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return self.inaccessible_callback(name, **kwargs)

        try:
            return _admin_guard()
        except Forbidden:
            return self.inaccessible_callback(name, **kwargs)

    def is_accessible(self):
        current_user = getattr(g, "current_user", None)
        return current_user is not None and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash("Admin access required", "error")
        return redirect(url_for("auth.login"))


class DashboardAdminIndexView(SecureAdminMixin, AdminIndexView):
    @expose("/")
    def index(self):
        today = date.today().isoformat()

        total_users = db.session.query(func.count(User.id)).scalar() or 0
        total_games_today = (
            Game.query.filter(func.date(Game.started_at) == today).count()
        )
        total_wins_today = (
            Game.query.filter(
                Game.status == "won",
                func.date(Game.ended_at) == today,
            ).count()
        )
        total_feedback_count = db.session.query(func.count(Feedback.id)).scalar() or 0

        return self.render(
            "admin/dashboard.html",
            total_users=total_users,
            total_games_today=total_games_today,
            total_wins_today=total_wins_today,
            total_feedback_count=total_feedback_count,
        )


class SecureModelView(SecureAdminMixin, ModelView):
    can_view_details = True
    page_size = 25


class UserAdmin(SecureModelView):
    column_list = ("id", "username", "email", "is_admin", "created_at")
    column_searchable_list = ("username", "email")
    column_filters = ("is_admin", "created_at")
    column_exclude_list = ("password_hash",)
    form_excluded_columns = ("password_hash", "games", "feedbacks")
    can_create = False

    @action(
        "reset_password",
        "Reset Password",
        "Reset the password for the selected users?",
    )
    def action_reset_password(self, ids):
        users = User.query.filter(User.id.in_(ids)).all()
        if not users:
            flash("No users were selected.", "error")
            return

        reset_messages = []
        for user in users:
            temporary_password = secrets.token_urlsafe(9)[:12]
            user.set_password(temporary_password)
            reset_messages.append(f"{user.username}: {temporary_password}")

        db.session.commit()
        flash(
            "Temporary passwords generated: " + "; ".join(reset_messages),
            "success",
        )


class GameAdmin(SecureModelView):
    column_list = ("id", "user", "difficulty", "status", "score", "attempts_used", "started_at")
    column_labels = {"user": "Username"}
    column_filters = ("difficulty", "status")
    can_create = False
    can_edit = False
    can_delete = False

    column_formatters = {
        "user": lambda view, context, model, name: model.user.username if model.user else "Unknown",
    }


class GuessAdmin(SecureModelView):
    column_list = ("id", "game_id", "guess_value", "result", "guessed_at")
    column_filters = ("result", "guessed_at")
    can_create = False
    can_edit = False
    can_delete = False


class FeedbackAdmin(SecureModelView):
    column_list = ("id", "user", "message", "submitted_at")
    column_labels = {"user": "Username"}
    can_create = False
    can_edit = False
    can_delete = True

    column_formatters = {
        "user": lambda view, context, model, name: model.user.username if model.user else "Anonymous",
    }


def register_admin_views(admin_extension) -> None:
    registered_endpoints = {
        getattr(view, "endpoint", None)
        for view in admin_extension._views
    }

    admin_views = (
        UserAdmin(User, db.session, endpoint="admin_users"),
        GameAdmin(Game, db.session, endpoint="admin_games"),
        GuessAdmin(Guess, db.session, endpoint="admin_guesses"),
        FeedbackAdmin(Feedback, db.session, endpoint="admin_feedback"),
    )

    for view in admin_views:
        if view.endpoint not in registered_endpoints:
            admin_extension.add_view(view)


def register_admin_commands(app) -> None:
    if "create-admin" in app.cli.commands:
        return

    @app.cli.command("create-admin")
    def create_admin_command():
        admin_email = app.config.get("ADMIN_EMAIL")
        admin_password = app.config.get("ADMIN_PASSWORD")

        if not admin_email or not admin_password:
            raise click.ClickException(
                "ADMIN_EMAIL and ADMIN_PASSWORD must be set before creating an admin."
            )

        existing_user = User.query.filter_by(email=admin_email).first()
        if existing_user:
            existing_user.is_admin = True
            existing_user.set_password(admin_password)
            db.session.commit()
            click.echo(
                f"Updated existing user '{existing_user.username}' with admin access."
            )
            return

        base_username = (admin_email.split("@", 1)[0] or "admin")[:80]
        username = base_username
        suffix = 1
        while User.query.filter_by(username=username).first():
            suffix_text = str(suffix)
            username = f"{base_username[: 80 - len(suffix_text)]}{suffix_text}"
            suffix += 1

        admin_user = User(
            username=username,
            email=admin_email,
            is_admin=True,
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()

        click.echo(f"Created admin user '{username}' using ADMIN_EMAIL credentials.")
