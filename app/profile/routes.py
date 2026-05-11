from flask import Blueprint, g, render_template
from sqlalchemy import func

from app.game.logic import DIFFICULTY_CONFIG
from app.auth.decorators import login_required
from app import db
from app.models import Game

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/", methods=["GET"], strict_slashes=False)
@login_required
def profile_index():
    user_id = g.current_user.id

    totals = (
        db.session.query(
            func.count(Game.id).label("total_games"),
            func.count().filter(Game.status == "won").label("total_wins"),
            func.max(Game.score).filter(Game.status == "won").label("best_score"),
        )
        .filter(Game.user_id == user_id)
        .one()
    )

    total_games = totals.total_games or 0
    total_wins = totals.total_wins or 0
    best_score = totals.best_score or 0
    win_rate = round((total_wins / total_games) * 100, 1) if total_games else 0.0

    difficulty_rows = (
        db.session.query(
            Game.difficulty,
            func.count(Game.id).label("count"),
        )
        .filter(Game.user_id == user_id)
        .group_by(Game.difficulty)
        .all()
    )
    difficulty_counts = {row.difficulty: row.count for row in difficulty_rows}
    games_by_difficulty = {
        difficulty: difficulty_counts.get(difficulty, 0)
        for difficulty in DIFFICULTY_CONFIG
    }

    recent_games = (
        Game.query.filter_by(user_id=user_id)
        .order_by(Game.started_at.desc(), Game.id.desc())
        .limit(10)
        .all()
    )

    return render_template(
        "profile.html",
        stats={
            "total_games": total_games,
            "total_wins": total_wins,
            "win_rate": win_rate,
            "best_score": best_score,
            "games_by_difficulty": games_by_difficulty,
        },
        recent_games=recent_games,
        user=g.current_user,
    )
