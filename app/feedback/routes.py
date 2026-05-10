from flask import Blueprint, flash, g, redirect, render_template, url_for

from app import db
from app.feedback.forms import FeedbackForm
from app.models import Feedback

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.route("/", methods=["GET", "POST"], strict_slashes=False)
def feedback_index():
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback(
            user_id=getattr(getattr(g, "current_user", None), "id", None),
            message=form.message.data.strip(),
        )
        db.session.add(feedback)
        db.session.commit()

        flash("Thanks for the feedback. Your message has been received.", "success")
        return redirect(url_for("feedback.feedback_index"))

    if form.is_submitted() and form.errors:
        flash("Please correct the feedback form errors below.", "error")

    return render_template("feedback.html", form=form)
