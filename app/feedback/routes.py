from flask import Blueprint, jsonify

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.get("/")
def feedback_index():
    # Feedback persistence depends on the database models added in the next phase.
    return jsonify({"blueprint": "feedback", "message": "Feedback endpoints arrive in Phase 8."}), 200
