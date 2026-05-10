import os
from datetime import timedelta


def _as_bool(value: str | None, default: bool = False) -> bool:
    """Parse common environment boolean values without raising."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///numberguesser.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # These seed values are kept in config now so later phases can reuse them
    # for admin bootstrap and operational tooling.
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_TOKEN_MINUTES", "15"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_REFRESH_TOKEN_DAYS", "7"))
    )
    JWT_TOKEN_LOCATION = ["headers", "cookies"]

    # Flask-WTF covers form CSRF now; JWT cookie CSRF can be tightened further
    # once the auth cookie flow is implemented in a later phase.
    JWT_COOKIE_CSRF_PROTECT = _as_bool(
        os.environ.get("JWT_COOKIE_CSRF_PROTECT"),
        default=False,
    )
    JWT_COOKIE_SECURE = _as_bool(
        os.environ.get("JWT_COOKIE_SECURE"),
        default=False,
    )


class DevelopmentConfig(BaseConfig):
    DEBUG = _as_bool(os.environ.get("FLASK_DEBUG"), default=True)
    ENV_NAME = "development"


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV_NAME = "production"
    JWT_COOKIE_SECURE = _as_bool(
        os.environ.get("JWT_COOKIE_SECURE"),
        default=True,
    )


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
