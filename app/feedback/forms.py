from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class FeedbackForm(FlaskForm):
    message = TextAreaField(
        "Your Feedback",
        validators=[
            DataRequired(),
            Length(min=80, message="Feedback must be at least 80 characters long."),
        ],
    )
    submit = SubmitField("Send Feedback")
