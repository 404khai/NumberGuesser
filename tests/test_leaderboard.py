from datetime import datetime, timedelta


def test_leaderboard_shows_top_players(client, create_game, create_user):
    first_user = create_user(username="alice", email="alice@example.com")
    second_user = create_user(username="bob", email="bob@example.com")

    create_game(
        user=first_user,
        difficulty="easy",
        secret_number=10,
        status="won",
        score=900,
        attempts_used=1,
        ended_at=datetime.utcnow(),
    )
    create_game(
        user=second_user,
        difficulty="expert",
        secret_number=500,
        status="won",
        score=700,
        attempts_used=2,
        ended_at=datetime.utcnow() + timedelta(seconds=1),
    )

    response = client.get("/leaderboard")
    page = response.data.decode("utf-8")

    assert response.status_code == 200
    assert "alice" in page
    assert "bob" in page
    assert page.index("alice") < page.index("bob")
    assert "Best: 900 | Wins: 1" in page


def test_leaderboard_filter_by_difficulty(client, create_game, create_user):
    easy_user = create_user(username="easyplayer", email="easy@example.com")
    expert_user = create_user(username="expertplayer", email="expert@example.com")

    create_game(
        user=easy_user,
        difficulty="easy",
        secret_number=12,
        status="won",
        score=800,
        ended_at=datetime.utcnow(),
    )
    create_game(
        user=expert_user,
        difficulty="expert",
        secret_number=999,
        status="won",
        score=1200,
        ended_at=datetime.utcnow() + timedelta(seconds=1),
    )

    response = client.get("/leaderboard?difficulty=easy")

    assert response.status_code == 200
    assert b"easyplayer" in response.data
    assert b"expertplayer" not in response.data
