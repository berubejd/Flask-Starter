from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy


# Globally accessible libraries
db = SQLAlchemy()


def not_found(e):
    return render_template("error.html"), 404


def create_app(test_config=None):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        app.config.from_object("config.Config")

    else:
        app.config.from_object("config.TestingConfig")

    # Initialize Plugins
    db.init_app(app)

    # Register Error Handlers
    app.register_error_handler(404, not_found)

    # Register Blueprints
    from . import routes

    app.register_blueprint(routes.main_bp)
    app.add_url_rule("/", endpoint="index")

    with app.app_context():
        # Setup the database
        from .models import Test

        db.create_all()

    return app
