import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Game


DIFFICULTY_CONFIG = {
    "easy": {"min": 0, "max": 99, "max_attempts": 10, "multiplier": 1},
    "moderate": {"min": 0, "max": 999, "max_attempts": 10, "multiplier": 2},
    "expert": {"min": 0, "max": 9999, "max_attempts": 10, "multiplier": 3},
}


def _get_difficulty_settings(difficulty: str) -> dict[str, int]:
    try:
        return DIFFICULTY_CONFIG[difficulty]
    except KeyError as exc:
        raise ValueError(f"Unsupported difficulty: {difficulty}") from exc


def generate_secret(difficulty: str) -> int:
    settings = _get_difficulty_settings(difficulty)
    return random.randint(settings["min"], settings["max"])


def evaluate_guess(secret: int, guess: int) -> str:
    if guess < secret:
        return "too_low"
    if guess > secret:
        return "too_high"
    return "correct"


def calculate_score(difficulty: str, attempts_used: int, max_attempts: int) -> int:
    settings = _get_difficulty_settings(difficulty)
    remaining_attempts = max_attempts - attempts_used
    return max(0, remaining_attempts * settings["multiplier"] * 100)


def attempts_remaining(game: "Game") -> int:
    return max(0, game.max_attempts - game.attempts_used)
