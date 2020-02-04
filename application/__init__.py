from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy


# Globally accessible libraries
db = SQLAlchemy()


def create_app(test_config=None):
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        app.config.from_object("config.Config")

    else:
        app.config.from_object("config.TestingConfig")

    # Initialize Plugins
    db.init_app(app)

    # Register Blueprints
    from . import routes

    app.register_blueprint(routes.main_bp)
    app.add_url_rule("/", endpoint="index")

    with app.app_context():
        # Setup the database
        from .models import Test

        db.create_all()

    return app
