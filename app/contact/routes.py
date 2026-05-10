from flask import Blueprint, render_template

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/", methods=["GET"], strict_slashes=False)
def contact_index():
    return render_template("contact.html")
