from datetime import datetime
from pathlib import Path
import sys

import pytest
from sqlalchemy.pool import StaticPool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app, db
from app.models import Game, User
from config import DevelopmentConfig


class TestConfig(DevelopmentConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }
    SERVER_NAME = "localhost"


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def create_user(app):
    def _create_user(
        username: str = "player1",
        email: str = "player1@example.com",
        password: str = "password123",
        is_admin: bool = False,
    ) -> User:
        user = User(username=username, email=email, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    return _create_user


@pytest.fixture
def create_game(app):
    def _create_game(
        user: User,
        difficulty: str = "easy",
        secret_number: int = 42,
        max_attempts: int = 10,
        attempts_used: int = 0,
        status: str = "active",
        score: int = 0,
        started_at: datetime | None = None,
        ended_at: datetime | None = None,
    ) -> Game:
        game = Game(
            user_id=user.id,
            difficulty=difficulty,
            secret_number=secret_number,
            max_attempts=max_attempts,
            attempts_used=attempts_used,
            status=status,
            score=score,
            started_at=started_at or datetime.utcnow(),
            ended_at=ended_at,
        )
        db.session.add(game)
        db.session.commit()
        return game

    return _create_game


@pytest.fixture
def test_user(create_user):
    return create_user()


@pytest.fixture
def admin_user(create_user):
    return create_user(
        username="adminuser",
        email="admin@example.com",
        is_admin=True,
    )


def _login(client, username: str, password: str):
    return client.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )


@pytest.fixture
def authenticated_client(client, test_user):
    response = _login(client, test_user.username, "password123")
    assert response.status_code == 302
    return client


@pytest.fixture
def admin_client(client, admin_user):
    response = _login(client, admin_user.username, "password123")
    assert response.status_code == 302
    return client
