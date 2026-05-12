from datetime import datetime

from flask import url_for

from app import db
from app.models import Feedback, Game, Guess, User


def test_non_admin_cannot_access_admin(authenticated_client):
    response = authenticated_client.get("/admin/", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/login")


def test_admin_can_access_admin(admin_client):
    response = admin_client.get("/admin/")

    assert response.status_code == 200
    assert b"NumberGuesser Admin" in response.data
    assert b"Dashboard" in response.data
    assert b"User" in response.data
    assert b"Game" in response.data
    assert b"Guess" in response.data
    assert b"Feedback" in response.data
    assert b"adminuser" in response.data
    assert b"admin-sidebar__link is-active" in response.data
    assert b"Home" in response.data
    assert b"/auth/logout" in response.data
    assert b"/auth/login" in response.data
    assert b"admin-confirm-overlay" in response.data


def test_admin_sidebar_highlights_active_model_view(admin_client, app):
    with app.test_request_context():
        user_admin_url = url_for("admin_users.index_view")

    response = admin_client.get(user_admin_url)

    assert response.status_code == 200
    assert b'admin-sidebar__link is-active"' in response.data
    assert b"Manage user records" in response.data


def test_admin_user_list_supports_promotion_and_order_controls(admin_client, app, create_user):
    promoted_user = create_user(username="member", email="member@example.com")

    with app.test_request_context():
        user_admin_url = url_for("admin_users.index_view")
        promote_url = url_for("admin_users.promote_view", user_id=promoted_user.id)

    response = admin_client.get(user_admin_url)

    assert response.status_code == 200
    assert b"Newest First" in response.data
    assert b"Oldest First" in response.data
    assert promote_url.encode() in response.data
    assert b"Promote User" in response.data
    assert b"Not Admin" in response.data


def test_admin_can_promote_user(admin_client, app, create_user):
    promoted_user = create_user(username="upgrade_me", email="upgrade@example.com")

    with app.test_request_context():
        promote_url = url_for("admin_users.promote_view", user_id=promoted_user.id)
        user_admin_url = url_for("admin_users.index_view")

    response = admin_client.post(
        promote_url,
        data={"url": user_admin_url},
        follow_redirects=False,
    )

    assert response.status_code == 302
    with app.app_context():
        refreshed_user = db.session.get(User, promoted_user.id)
        assert refreshed_user is not None
        assert refreshed_user.is_admin is True


def test_admin_game_and_guess_views_render_colored_badges(admin_client, app, admin_user, create_game):
    game = create_game(
        admin_user,
        difficulty="expert",
        status="won",
        started_at=datetime(2026, 5, 11, 18, 17),
    )
    with app.app_context():
        db.session.add(
            Guess(
                game_id=game.id,
                guess_value=42,
                result="too_high",
                guessed_at=datetime(2026, 5, 11, 18, 17),
            )
        )
        db.session.commit()

    with app.test_request_context():
        games_url = url_for("admin_games.index_view")
        guesses_url = url_for("admin_guesses.index_view")

    games_response = admin_client.get(games_url)
    guesses_response = admin_client.get(guesses_url)

    assert games_response.status_code == 200
    assert b"admin-badge admin-badge--expert" in games_response.data
    assert b"admin-badge admin-badge--success" in games_response.data

    assert guesses_response.status_code == 200
    assert b"admin-badge admin-badge--danger" in guesses_response.data
    assert b"11-05-2026  6:17pm" in guesses_response.data


def test_admin_feedback_details_wrap_message_and_format_time(admin_client, app, admin_user):
    with app.app_context():
        feedback = Feedback(
            user_id=admin_user.id,
            message="This is a long feedback message " * 12,
            submitted_at=datetime(2026, 5, 11, 18, 17),
        )
        db.session.add(feedback)
        db.session.commit()
        feedback_id = feedback.id

    with app.test_request_context():
        feedback_details_url = url_for("admin_feedback.details_view", id=feedback_id)

    response = admin_client.get(feedback_details_url)

    assert response.status_code == 200
    assert b"admin-message-detail" in response.data
    assert b"11-05-2026  6:17pm" in response.data
