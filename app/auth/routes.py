from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/")
def auth_index():
    # Auth flows are implemented in Phase 3; this keeps the blueprint live now.
    return jsonify({"blueprint": "auth", "message": "Authentication endpoints arrive in Phase 3."}), 200
