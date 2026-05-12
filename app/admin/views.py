import secrets
from datetime import date, datetime

import click
from flask import flash, g, redirect, request, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.actions import action
from flask_admin.contrib.sqla import ModelView
from flask_wtf.csrf import generate_csrf
from markupsafe import Markup, escape
from sqlalchemy import func
from werkzeug.exceptions import Forbidden

from app import db
from app.auth.decorators import admin_required
from app.models import Feedback, Game, Guess, User


@admin_required
def _admin_guard():
    return None


def _format_admin_datetime(value: datetime | None) -> str:
    if value is None:
        return "N/A"

    hour = value.strftime("%I").lstrip("0") or "0"
    return f"{value.strftime('%d-%m-%Y')}  {hour}:{value.strftime('%M')}{value.strftime('%p').lower()}"


def _render_badge(label: str, modifier: str) -> Markup:
    return Markup(
        f'<span class="admin-badge admin-badge--{modifier}">{escape(label)}</span>'
    )


def _render_boolean_status(value: bool) -> Markup:
    if value:
        return Markup(
            '<span class="admin-flag admin-flag--true" aria-label="Admin">'
            '<span class="admin-flag__icon">&#10003;</span>'
            '<span>Admin</span>'
            "</span>"
        )

    return Markup(
        '<span class="admin-flag admin-flag--false" aria-label="Not admin">'
        '<span class="admin-flag__icon">&minus;</span>'
        '<span>Not Admin</span>'
        "</span>"
    )


def _render_promote_button(view, model) -> str:
    if getattr(model, "is_admin", False):
        return ""

    promote_url = view.get_url(".promote_view", user_id=model.id)
    return_url = escape(request.url)
    csrf_token = escape(generate_csrf())
    username = escape(getattr(model, "username", "this user"))

    return (
        '<form class="admin-inline-form" method="POST" '
        f'action="{escape(promote_url)}" '
        'data-confirm-form="true" '
        'data-confirm-title="Promote User" '
        f'data-confirm-message="Promote {username} to admin?"'
        ">"
        f'<input type="hidden" name="csrf_token" value="{csrf_token}">'
        f'<input type="hidden" name="url" value="{return_url}">'
        '<button class="admin-inline-action admin-inline-action--promote" '
        'type="submit" title="Promote user to admin" aria-label="Promote user to admin">'
        '<span class="admin-inline-action__icon">&#8593;</span>'
        "</button>"
        "</form>"
    )


def _format_user_admin_status(view, context, model, name):
    return Markup(
        '<div class="admin-boolean-cell">'
        f"{_render_boolean_status(model.is_admin)}"
        f"{_render_promote_button(view, model)}"
        "</div>"
    )


def _format_datetime_column(view, context, model, name):
    return _format_admin_datetime(getattr(model, name))


def _format_user_column(view, context, model, name):
    return escape(model.user.username if model.user else "Unknown")


def _format_difficulty_column(view, context, model, name):
    return _render_badge(model.difficulty.title(), model.difficulty)


def _format_status_column(view, context, model, name):
    status_map = {
        "active": "info",
        "won": "success",
        "lost": "danger",
    }
    return _render_badge(model.status.title(), status_map.get(model.status, "neutral"))


def _format_result_column(view, context, model, name):
    label_map = {
        "too_low": "Too Low",
        "too_high": "Too High",
        "correct": "Correct",
    }
    badge_map = {
        "too_low": "success",
        "too_high": "danger",
        "correct": "info",
    }
    return _render_badge(
        label_map.get(model.result, model.result.replace("_", " ").title()),
        badge_map.get(model.result, "neutral"),
    )


def _format_feedback_message_list(view, context, model, name):
    message = (model.message or "").strip()
    if len(message) > 120:
        message = f"{message[:117]}..."
    return Markup(f'<div class="admin-message-snippet">{escape(message)}</div>')


def _format_feedback_message_detail(view, context, model, name):
    return Markup(
        f'<div class="admin-message-detail">{escape(model.message or "")}</div>'
    )


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
    list_template = "admin/model/list_custom.html"
    time_sort_column = None

    def get_time_sort_index(self):
        if not self.time_sort_column:
            return None

        for index, (column_name, _label) in enumerate(self.get_list_columns()):
            if column_name == self.time_sort_column:
                return index
        return None

    def get_time_order_url(self, descending: bool):
        sort_index = self.get_time_sort_index()
        if sort_index is None:
            return None

        view_args = self._get_list_extra_args().clone(
            page=0,
            sort=sort_index,
            sort_desc=descending,
        )
        return self._get_list_url(view_args)

    def is_desc_time_order(self):
        sort_index = self.get_time_sort_index()
        if sort_index is None:
            return True

        view_args = self._get_list_extra_args()
        if view_args.sort == sort_index:
            return bool(view_args.sort_desc)
        return True


class UserAdmin(SecureModelView):
    column_list = ("id", "username", "email", "is_admin", "created_at")
    column_searchable_list = ("username", "email")
    column_filters = ("is_admin", "created_at")
    column_exclude_list = ("password_hash",)
    form_excluded_columns = ("password_hash", "games", "feedbacks")
    can_create = False
    can_edit = False
    time_sort_column = "created_at"
    column_default_sort = ("created_at", True)
    column_formatters = {
        "is_admin": _format_user_admin_status,
        "created_at": _format_datetime_column,
    }
    column_formatters_detail = {
        "is_admin": _format_user_admin_status,
        "created_at": _format_datetime_column,
    }

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

    @expose("/promote/<int:user_id>", methods=("POST",))
    def promote_view(self, user_id):
        user = db.session.get(User, user_id)
        if user is None:
            flash("User not found.", "error")
            return redirect(self.get_url(".index_view"))

        if user.is_admin:
            flash(f"{user.username} is already an admin.", "info")
            return redirect(request.form.get("url") or self.get_url(".index_view"))

        user.is_admin = True
        db.session.commit()
        flash(f"{user.username} has been promoted to admin.", "success")
        return redirect(request.form.get("url") or self.get_url(".index_view"))


class GameAdmin(SecureModelView):
    column_list = (
        "id",
        "user",
        "difficulty",
        "status",
        "score",
        "attempts_used",
        "started_at",
    )
    column_labels = {"user": "Username"}
    column_filters = ("difficulty", "status")
    can_create = False
    can_edit = False
    can_delete = False
    time_sort_column = "started_at"
    column_default_sort = ("started_at", True)
    column_formatters = {
        "user": _format_user_column,
        "difficulty": _format_difficulty_column,
        "status": _format_status_column,
        "started_at": _format_datetime_column,
        "ended_at": _format_datetime_column,
    }
    column_formatters_detail = {
        "user": _format_user_column,
        "difficulty": _format_difficulty_column,
        "status": _format_status_column,
        "started_at": _format_datetime_column,
        "ended_at": _format_datetime_column,
    }


class GuessAdmin(SecureModelView):
    column_list = ("id", "game_id", "guess_value", "result", "guessed_at")
    column_filters = ("result", "guessed_at")
    can_create = False
    can_edit = False
    can_delete = False
    time_sort_column = "guessed_at"
    column_default_sort = ("guessed_at", True)
    column_formatters = {
        "result": _format_result_column,
        "guessed_at": _format_datetime_column,
    }
    column_formatters_detail = {
        "result": _format_result_column,
        "guessed_at": _format_datetime_column,
    }


class FeedbackAdmin(SecureModelView):
    column_list = ("id", "user", "message", "submitted_at")
    column_labels = {"user": "Username"}
    can_create = False
    can_edit = False
    can_delete = True
    time_sort_column = "submitted_at"
    column_default_sort = ("submitted_at", True)
    column_formatters = {
        "user": _format_user_column,
        "message": _format_feedback_message_list,
        "submitted_at": _format_datetime_column,
    }
    column_formatters_detail = {
        "user": _format_user_column,
        "message": _format_feedback_message_detail,
        "submitted_at": _format_datetime_column,
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
