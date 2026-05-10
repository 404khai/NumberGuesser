from flask import Blueprint, jsonify

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.get("/")
def leaderboard_index():
    # A lightweight placeholder lets the route prefix exist before scoring logic is added.
    return jsonify({"blueprint": "leaderboard", "message": "Leaderboard endpoints arrive in Phase 5."}), 200
