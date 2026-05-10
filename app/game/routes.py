from flask import Blueprint, render_template

from app.auth.decorators import login_required

game_bp = Blueprint("game", __name__)


@game_bp.get("/")
@login_required
def game_index():
    return render_template("game/select.html")


@game_bp.get("/select")
@login_required
def select_game():
    # Phase 4 will replace this placeholder with difficulty selection logic.
    return render_template("game/select.html")
