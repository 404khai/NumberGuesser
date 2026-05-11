from app import db
from app.models import User


def test_register_success(client, app):
    response = client.post(
        "/auth/register",
        data={
            "username": "newplayer",
            "email": "newplayer@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/login")

    with app.app_context():
        user = User.query.filter_by(username="newplayer").first()
        assert user is not None
        assert user.email == "newplayer@example.com"
        assert user.check_password("Password123!")


def test_register_duplicate_username(client, app, test_user):
    response = client.post(
        "/auth/register",
        data={
            "username": test_user.username,
            "email": "another@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"That username is already taken." in response.data

    with app.app_context():
        assert User.query.count() == 1


def test_register_password_mismatch(client, app):
    response = client.post(
        "/auth/register",
        data={
            "username": "mismatch",
            "email": "mismatch@example.com",
            "password": "Password123!",
            "confirm_password": "Password124!",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Passwords must match." in response.data

    with app.app_context():
        assert User.query.filter_by(username="mismatch").first() is None


def test_register_requires_strong_password(client, app):
    response = client.post(
        "/auth/register",
        data={
            "username": "weakpass",
            "email": "weakpass@example.com",
            "password": "password123",
            "confirm_password": "password123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Password must include at least one uppercase letter." in response.data

    with app.app_context():
        assert User.query.filter_by(username="weakpass").first() is None


def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user.username, "password": "password123"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/game/select")
    cookies = response.headers.getlist("Set-Cookie")
    assert any("access_token_cookie=" in cookie for cookie in cookies)


def test_login_success_with_email(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user.email, "password": "password123"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/game/select")


def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login",
        data={"username": test_user.username, "password": "wrongpass1"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid credentials." in response.data
    assert "access_token_cookie=" not in " ".join(response.headers.getlist("Set-Cookie"))


def test_logout(authenticated_client):
    response = authenticated_client.get("/auth/logout", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    cookies = response.headers.getlist("Set-Cookie")
    assert any("access_token_cookie=;" in cookie for cookie in cookies)
