from app import db
from app.models import Game, Guess


def test_start_game_easy(authenticated_client, app, test_user, monkeypatch):
    monkeypatch.setattr("app.game.routes.generate_secret", lambda difficulty: 17)

    response = authenticated_client.post(
        "/game/start",
        data={"difficulty": "easy"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/game/play")

    with app.app_context():
        game = Game.query.filter_by(user_id=test_user.id).one()
        assert game.difficulty == "easy"
        assert game.status == "active"
        assert game.secret_number == 17
        assert game.max_attempts == 10


def test_start_game_creates_secret_in_range(authenticated_client, app, test_user):
    response = authenticated_client.post(
        "/game/start",
        data={"difficulty": "easy"},
        follow_redirects=False,
    )

    assert response.status_code == 302

    with app.app_context():
        game = Game.query.filter_by(user_id=test_user.id).one()
        assert 0 <= game.secret_number <= 99


def test_guess_too_low(authenticated_client, app, create_game, test_user):
    game = create_game(user=test_user, secret_number=50)

    response = authenticated_client.post(
        "/game/guess",
        data={"guess": "10"},
        follow_redirects=False,
    )

    assert response.status_code == 200
    assert b"too low" in response.data.lower()

    with app.app_context():
        game = db.session.get(Game, game.id)
        assert game.attempts_used == 1
        assert game.status == "active"
        guess = Guess.query.filter_by(game_id=game.id).one()
        assert guess.result == "too_low"


def test_guess_too_high(authenticated_client, app, create_game, test_user):
    game = create_game(user=test_user, secret_number=50)

    response = authenticated_client.post(
        "/game/guess",
        data={"guess": "90"},
        follow_redirects=False,
    )

    assert response.status_code == 200
    assert b"too high" in response.data.lower()

    with app.app_context():
        game = db.session.get(Game, game.id)
        assert game.attempts_used == 1
        guess = Guess.query.filter_by(game_id=game.id).one()
        assert guess.result == "too_high"


def test_guess_correct_sets_won(authenticated_client, app, create_game, test_user):
    game = create_game(user=test_user, secret_number=50)

    response = authenticated_client.post(
        "/game/guess",
        data={"guess": "50"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/game/result")

    with app.app_context():
        game = db.session.get(Game, game.id)
        assert game.status == "won"
        assert game.ended_at is not None


def test_guess_correct_calculates_score(authenticated_client, app, create_game, test_user):
    game = create_game(
        user=test_user,
        secret_number=50,
        attempts_used=2,
        max_attempts=10,
    )

    authenticated_client.post(
        "/game/guess",
        data={"guess": "50"},
        follow_redirects=False,
    )

    with app.app_context():
        game = db.session.get(Game, game.id)
        assert game.score == 700


def test_max_attempts_reached_sets_lost(authenticated_client, app, create_game, test_user):
    game = create_game(
        user=test_user,
        secret_number=50,
        attempts_used=9,
        max_attempts=10,
    )

    response = authenticated_client.post(
        "/game/guess",
        data={"guess": "10"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/game/result")

    with app.app_context():
        game = db.session.get(Game, game.id)
        assert game.status == "lost"
        assert game.score == 0
        assert game.ended_at is not None


def test_guess_out_of_range_rejected(authenticated_client, app, create_game, test_user):
    game = create_game(user=test_user, secret_number=50)

    response = authenticated_client.post(
        "/game/guess",
        data={"guess": "101"},
        follow_redirects=False,
    )

    assert response.status_code == 400
    assert b"Guess must be between 0 and 99." in response.data

    with app.app_context():
        game = db.session.get(Game, game.id)
        assert game.attempts_used == 0
        assert Guess.query.filter_by(game_id=game.id).count() == 0


def test_guess_non_integer_rejected(authenticated_client, app, create_game, test_user):
    game = create_game(user=test_user, secret_number=50)

    response = authenticated_client.post(
        "/game/guess",
        data={"guess": "not-a-number"},
        follow_redirects=False,
    )

    assert response.status_code == 400
    assert b"Enter a whole number within the allowed range." in response.data

    with app.app_context():
        game = db.session.get(Game, game.id)
        assert game.attempts_used == 0
        assert Guess.query.filter_by(game_id=game.id).count() == 0
