from datetime import datetime

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.auth.decorators import login_required
from app.game.logic import (
    DIFFICULTY_CONFIG,
    attempts_remaining,
    calculate_score,
    evaluate_guess,
    generate_secret,
)
from app.leaderboard.routes import get_game_rank
from app import db
from app.models import Game, Guess

game_bp = Blueprint("game", __name__)


@game_bp.get("/")
@login_required
def game_index():
    return redirect(url_for("game.select_game"))


@game_bp.get("/select")
@login_required
def select_game():
    active_game = _get_active_game()
    return render_template(
        "game/select.html",
        active_game=active_game,
        difficulty_config=DIFFICULTY_CONFIG,
    )


@game_bp.post("/start")
@login_required
def start_game():
    difficulty = (request.form.get("difficulty") or "").strip().lower()
    if difficulty not in DIFFICULTY_CONFIG:
        flash("Please choose a valid difficulty.", "error")
        return redirect(url_for("game.select_game"))

    active_game = _get_active_game()
    if active_game is not None:
        active_game.status = "lost"
        active_game.score = 0
        active_game.ended_at = datetime.utcnow()

    settings = DIFFICULTY_CONFIG[difficulty]
    new_game = Game(
        user_id=g.current_user.id,
        difficulty=difficulty,
        secret_number=generate_secret(difficulty),
        max_attempts=settings["max_attempts"],
        attempts_used=0,
        status="active",
        score=0,
    )
    db.session.add(new_game)
    db.session.commit()

    flash(f"New {difficulty.title()} game started. Good luck!", "success")
    return redirect(url_for("game.play_game"))


@game_bp.get("/play")
@login_required
def play_game():
    active_game = _get_active_game()
    if active_game is None:
        flash("Start a game before making guesses.", "info")
        return redirect(url_for("game.select_game"))

    return render_template(
        "game/play.html",
        game=active_game,
        guesses=list(reversed(active_game.guesses)),
        config=DIFFICULTY_CONFIG[active_game.difficulty],
        difficulty_settings=DIFFICULTY_CONFIG[active_game.difficulty],
        remaining_attempts=attempts_remaining(active_game),
        guess_history=active_game.guesses,
        last_feedback=_build_last_feedback(active_game),
    )


@game_bp.post("/guess")
@login_required
def submit_guess():
    active_game = _get_active_game()
    if active_game is None:
        flash("There is no active game to play.", "error")
        return redirect(url_for("game.select_game"))

    difficulty_settings = DIFFICULTY_CONFIG[active_game.difficulty]
    guess_value_raw = (request.form.get("guess") or "").strip()

    try:
        guess_value = int(guess_value_raw)
    except ValueError:
        flash("Enter a whole number within the allowed range.", "error")
        return _render_play_state(active_game), 400

    if not difficulty_settings["min"] <= guess_value <= difficulty_settings["max"]:
        flash(
            f"Guess must be between {difficulty_settings['min']} and {difficulty_settings['max']}.",
            "error",
        )
        return _render_play_state(active_game), 400

    result = evaluate_guess(active_game.secret_number, guess_value)
    active_game.attempts_used += 1

    guess = Guess(
        game_id=active_game.id,
        guess_value=guess_value,
        result=result,
    )
    db.session.add(guess)

    if result == "correct":
        active_game.status = "won"
        active_game.ended_at = datetime.utcnow()
        active_game.score = calculate_score(
            active_game.difficulty,
            active_game.attempts_used,
            active_game.max_attempts,
        )
        db.session.commit()
        flash("Correct guess. You won!", "success")
        return redirect(url_for("game.game_result"))

    if active_game.attempts_used >= active_game.max_attempts:
        active_game.status = "lost"
        active_game.ended_at = datetime.utcnow()
        active_game.score = 0
        db.session.commit()
        flash(
            f"Out of attempts. The number was {active_game.secret_number}.",
            "info",
        )
        return redirect(url_for("game.game_result"))

    db.session.commit()
    flash(_build_last_feedback(active_game), "info")
    return redirect(url_for("game.play_game"))


@game_bp.get("/result")
@login_required
def game_result():
    completed_game = _get_last_completed_game()
    if completed_game is None:
        flash("Finish a game to see the result screen.", "info")
        return redirect(url_for("game.select_game"))

    return render_template(
        "game/result.html",
        game=completed_game,
        difficulty_settings=DIFFICULTY_CONFIG[completed_game.difficulty],
        remaining_attempts=attempts_remaining(completed_game),
        leaderboard_rank=get_game_rank(completed_game),
    )


def _get_active_game():
    return (
        Game.query.filter_by(user_id=g.current_user.id, status="active")
        .order_by(Game.started_at.desc(), Game.id.desc())
        .first()
    )


def _get_last_completed_game():
    return (
        Game.query.filter(
            Game.user_id == g.current_user.id,
            Game.status.in_(("won", "lost")),
        )
        .order_by(Game.ended_at.desc(), Game.id.desc())
        .first()
    )


def _build_last_feedback(game: Game) -> str | None:
    if not game.guesses:
        return None

    latest_guess = game.guesses[-1]
    if latest_guess.result == "too_low":
        return f"{latest_guess.guess_value} was too low. Try a higher number."
    if latest_guess.result == "too_high":
        return f"{latest_guess.guess_value} was too high. Try a lower number."
    return f"{latest_guess.guess_value} was correct."


def _render_play_state(game: Game):
    return render_template(
        "game/play.html",
        game=game,
        guesses=list(reversed(game.guesses)),
        config=DIFFICULTY_CONFIG[game.difficulty],
        difficulty_settings=DIFFICULTY_CONFIG[game.difficulty],
        remaining_attempts=attempts_remaining(game),
        guess_history=game.guesses,
        last_feedback=_build_last_feedback(game),
    )
