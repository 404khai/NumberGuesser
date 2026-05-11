from flask import Blueprint, g, render_template, request
from sqlalchemy import and_, func, or_

from app import db
from app.game.logic import DIFFICULTY_CONFIG
from app.models import Game, User

leaderboard_bp = Blueprint("leaderboard", __name__)

VALID_FILTERS = ("all", "easy", "moderate", "expert")


@leaderboard_bp.route("/", methods=["GET"], strict_slashes=False)
def leaderboard_index():
    selected_difficulty = (request.args.get("difficulty") or "all").strip().lower()
    if selected_difficulty not in VALID_FILTERS:
        selected_difficulty = "all"

    leaderboard_query = (
        db.session.query(Game, User)
        .join(User, User.id == Game.user_id)
        .filter(Game.status == "won")
    )

    if selected_difficulty != "all":
        leaderboard_query = leaderboard_query.filter(Game.difficulty == selected_difficulty)

    leaderboard_games = (
        leaderboard_query
        .order_by(Game.score.desc(), Game.ended_at.asc(), Game.id.asc())
        .limit(20)
        .all()
    )

    user_stats_query = (
        db.session.query(
            Game.user_id,
            func.max(Game.score).label("best_score"),
            func.count(Game.id).label("total_wins"),
        )
        .filter(Game.status == "won")
    )
    if selected_difficulty != "all":
        user_stats_query = user_stats_query.filter(Game.difficulty == selected_difficulty)

    user_stats = {
        row.user_id: {
            "best_score": row.best_score,
            "total_wins": row.total_wins,
        }
        for row in user_stats_query.group_by(Game.user_id).all()
    }

    entries = []
    current_user_id = getattr(getattr(g, "current_user", None), "id", None)
    for index, (game, user) in enumerate(leaderboard_games, start=1):
        stats = user_stats.get(game.user_id, {"best_score": game.score, "total_wins": 1})
        entries.append(
            {
                "rank": index,
                "game": game,
                "user": user,
                "best_score": stats["best_score"],
                "total_wins": stats["total_wins"],
                "is_current_user": current_user_id == user.id,
            }
        )

    return render_template(
        "leaderboard.html",
        entries=entries,
        difficulty_config=DIFFICULTY_CONFIG,
        selected_difficulty=selected_difficulty,
        current_difficulty=None if selected_difficulty == "all" else selected_difficulty,
        current_user=getattr(g, "current_user", None),
    )


def get_game_rank(game: Game, difficulty: str | None = None) -> int | None:
    if game.status != "won":
        return None

    ahead_query = Game.query.filter(Game.status == "won")
    if difficulty is not None:
        ahead_query = ahead_query.filter(Game.difficulty == difficulty)

    ahead_query = ahead_query.filter(
        or_(
            Game.score > game.score,
            and_(Game.score == game.score, Game.ended_at < game.ended_at),
            and_(
                Game.score == game.score,
                Game.ended_at == game.ended_at,
                Game.id < game.id,
            ),
        )
    )
    return ahead_query.count() + 1
