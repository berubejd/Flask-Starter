from flask import Flask, render_template
from config import Config
from .models import db
from .views import main_blueprint


def not_found(e):
    return render_template("error.html"), 404


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Initialize Plugins
    db.init_app(app)

    # Register Error Handlers
    app.register_error_handler(404, not_found)

    # Register Blueprints
    app.register_blueprint(main_blueprint)
    app.add_url_rule("/", endpoint="index")

    with app.app_context():
        # Setup the database
        from .models import Test

        db.create_all()

    return app
