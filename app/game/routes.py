from flask import Blueprint, jsonify

game_bp = Blueprint("game", __name__)


@game_bp.get("/")
def game_index():
    # Gameplay is intentionally deferred until the dedicated game-engine phase.
    return jsonify({"blueprint": "game", "message": "Gameplay endpoints arrive in Phase 4."}), 200
