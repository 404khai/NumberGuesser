from datetime import datetime, timedelta

from app.models import Feedback


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
    assert b"Top 5 players" in response.data
    assert b"previewuser" in response.data


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
