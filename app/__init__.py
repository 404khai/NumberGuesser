import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import DevelopmentConfig, config_by_name

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
csrf = CSRFProtect()

# The admin shell is initialized now so future phases only need to register views.
admin = Admin(name="NumberGuesser Admin", template_mode="bootstrap4")


class BasicModelView(ModelView):
    can_view_details = True
    page_size = 25


def create_app(config_class=None) -> Flask:
    """Application factory used by the Flask CLI, tests, and `run.py`."""
    load_dotenv()

    app = Flask(__name__)
    env_name = os.environ.get("FLASK_ENV", "development")
    selected_config = config_class or config_by_name.get(env_name, DevelopmentConfig)
    app.config.from_object(selected_config)

    _init_extensions(app)
    _register_admin_views()
    _register_core_routes(app)
    _register_blueprints(app)
    _register_jwt_error_handlers()

    return app


def _init_extensions(app: Flask) -> None:
    # Import models before migrations/admin registration so metadata is available.
    from app import models  # noqa: F401

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)
    admin.init_app(app)


def _register_admin_views() -> None:
    from app.models import Feedback, Game, Guess, User

    registered_models = {
        getattr(view, "model", None)
        for view in admin._views
    }

    for model in (User, Game, Guess, Feedback):
        if model not in registered_models:
            admin.add_view(
                BasicModelView(
                    model,
                    db.session,
                    endpoint=f"admin_{model.__tablename__}",
                )
            )


def _register_core_routes(app: Flask) -> None:
    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok"}), 200

    @app.get("/")
    def index():
        return jsonify(
            {
                "app": "NumberGuesser",
                "message": "Project scaffold is ready.",
            }
        ), 200


def _register_blueprints(app: Flask) -> None:
    # Import inside the factory path so extension singletons stay import-safe.
    from app.auth import auth_bp
    from app.contact import contact_bp
    from app.feedback import feedback_bp
    from app.game import game_bp
    from app.leaderboard import leaderboard_bp
    from app.profile import profile_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(game_bp, url_prefix="/game")
    app.register_blueprint(leaderboard_bp, url_prefix="/leaderboard")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(contact_bp, url_prefix="/contact")
    app.register_blueprint(feedback_bp, url_prefix="/feedback")


def _register_jwt_error_handlers() -> None:
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_message):
        return jsonify({"error": "invalid_token", "message": error_message}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error_message):
        return jsonify({"error": "authorization_required", "message": error_message}), 401

    @jwt.needs_fresh_token_loader
    def fresh_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "fresh_token_required"}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "token_revoked"}), 401
