from datetime import datetime

from app import bcrypt, db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    games = db.relationship(
        "Game",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan",
    )
    feedbacks = db.relationship(
        "Feedback",
        back_populates="user",
        lazy=True,
    )

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Game(db.Model):
    __tablename__ = "games"

    DIFFICULTY_MULTIPLIERS = {
        "easy": 1,
        "moderate": 2,
        "expert": 3,
    }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    secret_number = db.Column(db.Integer, nullable=False)
    max_attempts = db.Column(db.Integer, default=10, nullable=False)
    attempts_used = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(20), default="active", nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ended_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.CheckConstraint(
            "difficulty IN ('easy', 'moderate', 'expert')",
            name="ck_games_difficulty",
        ),
        db.CheckConstraint(
            "status IN ('active', 'won', 'lost')",
            name="ck_games_status",
        ),
    )

    user = db.relationship("User", back_populates="games")
    guesses = db.relationship(
        "Guess",
        back_populates="game",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Guess.guessed_at.asc()",
    )

    @staticmethod
    def calculate_score(difficulty: str, attempts_used: int, max_attempts: int) -> int:
        multiplier = Game.DIFFICULTY_MULTIPLIERS.get(difficulty, 0)
        remaining_attempts = max_attempts - attempts_used
        return max(0, remaining_attempts * multiplier * 100)

    def __repr__(self) -> str:
        return f"<Game {self.id} {self.difficulty} {self.status}>"


class Guess(db.Model):
    __tablename__ = "guesses"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    guess_value = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(20), nullable=False)
    guessed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            "result IN ('too_high', 'too_low', 'correct')",
            name="ck_guesses_result",
        ),
    )

    game = db.relationship("Game", back_populates="guesses")

    def __repr__(self) -> str:
        return f"<Guess {self.id} {self.result}>"


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="feedbacks")

    def __repr__(self) -> str:
        return f"<Feedback {self.id} user_id={self.user_id}>"
