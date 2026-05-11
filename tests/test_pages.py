from datetime import datetime, timedelta

from app import db
from app.models import Feedback, Guess


def test_home_page_renders_leaderboard_preview(client, create_user, create_game):
    player = create_user(username="previewuser", email="preview@example.com")
    create_game(
        user=player,
        difficulty="moderate",
        secret_number=250,
        status="won",
        score=1200,
        ended_at=datetime.utcnow(),
    )

    response = client.get("/")

    assert response.status_code == 200
    assert b"Can You Guess the Number?" in response.data
    assert b"The best of the best. Updated in real time." in response.data
    assert b"previewuser" in response.data
    assert b"difficulty-pill difficulty-pill--moderate" in response.data


def test_health_check_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_contact_page_renders(client):
    response = client.get("/contact")

    assert response.status_code == 200
    assert b"Aptech Learning" in response.data
    assert b"support@aptech.com" in response.data


def test_feedback_requires_login(client):
    response = client.get("/feedback", follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_public_pages_ignore_stale_auth_cookie(client):
    client.set_cookie("access_token_cookie", "expired-or-invalid-token")

    home_response = client.get("/")
    leaderboard_response = client.get("/leaderboard/")

    assert home_response.status_code == 200
    assert leaderboard_response.status_code == 200


def test_protected_pages_clear_stale_auth_cookie(client):
    client.set_cookie("access_token_cookie", "expired-or-invalid-token")

    response = client.get("/game/select", follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]
    assert any(
        "access_token_cookie=;" in cookie
        for cookie in response.headers.getlist("Set-Cookie")
    )


def test_feedback_submission_saves_logged_in_user(authenticated_client, app, test_user):
    message = "This is detailed product feedback that is definitely longer than eighty characters for validation."

    response = authenticated_client.post(
        "/feedback",
        data={"message": message},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/feedback/")

    with app.app_context():
        feedback = Feedback.query.one()
        assert feedback.user_id == test_user.id
        assert feedback.message == message


def test_profile_shows_stats_and_recent_games(authenticated_client, create_game, test_user):
    create_game(
        user=test_user,
        difficulty="easy",
        secret_number=10,
        status="won",
        score=900,
        attempts_used=1,
        started_at=datetime.utcnow(),
        ended_at=datetime.utcnow(),
    )
    selected_game = create_game(
        user=test_user,
        difficulty="expert",
        secret_number=999,
        status="lost",
        score=0,
        attempts_used=10,
        started_at=datetime.utcnow() + timedelta(seconds=1),
        ended_at=datetime.utcnow() + timedelta(seconds=2),
    )

    response = authenticated_client.get(f"/profile?game={selected_game.id}")

    assert response.status_code == 200
    assert b"Total Games" in response.data
    assert b"Win Rate" in response.data
    assert b"expert" in response.data.lower()
    assert b"900" in response.data


def test_profile_requires_login(client):
    response = client.get("/profile", follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_play_page_shows_complete_guess_history(authenticated_client, app, create_game, test_user):
    game = create_game(user=test_user, difficulty="easy", secret_number=50)

    with app.app_context():
        db.session.add_all(
            [
                Guess(game_id=game.id, guess_value=10, result="too_low"),
                Guess(game_id=game.id, guess_value=70, result="too_high"),
                Guess(game_id=game.id, guess_value=50, result="correct"),
            ]
        )
        game.attempts_used = 3
        db.session.commit()

    response = authenticated_client.get("/game/play")

    assert response.status_code == 200
    assert b"3 total" in response.data
    assert b"10" in response.data
    assert b"70" in response.data
    assert b"50" in response.data
