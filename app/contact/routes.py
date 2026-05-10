from flask import Blueprint, jsonify

contact_bp = Blueprint("contact", __name__)


@contact_bp.get("/")
def contact_index():
    # Contact content is added later, but the public blueprint is scaffolded now.
    return jsonify({"blueprint": "contact", "message": "Contact page arrives in Phase 8."}), 200
