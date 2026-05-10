from flask import Blueprint, jsonify

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("/")
def profile_index():
    # User profile aggregation depends on models and auth, which are added later.
    return jsonify({"blueprint": "profile", "message": "Profile endpoints arrive in Phase 6."}), 200
