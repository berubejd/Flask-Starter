from flask import Flask, render_template
from config import Config
from .blueprints import auth_blueprint, main_blueprint
from .models import bcrypt, db, login_manager
from .oauth import facebook_blueprint, google_blueprint


def not_found(e):
    return render_template("error.j2"), 404


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Initialize Plugins
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register Error Handlers
    app.register_error_handler(404, not_found)

    # Register Blueprints
    app.register_blueprint(facebook_blueprint, url_prefix="/login")
    app.register_blueprint(google_blueprint, url_prefix="/login")
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.add_url_rule("/", endpoint="index")

    with app.app_context():
        # Setup the database
        from .models import User, OAuth

        db.create_all()

    return app
