import os
from pathlib import Path


class Config:
    """Set Flask configuration vars."""

    # General Config
    FLASK_APP = os.environ.get("FLASK_APP") or "application"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"

    ENV = os.environ.get("FLASK_ENV") or "development"
    if ENV == "development":
        DEBUG = True

    # SQLAlchemy Config
    if "RDS_HOSTNAME" in os.environ:
        NAME = os.environ["RDS_DB_NAME"]
        USER = os.environ["RDS_USERNAME"]
        PASSWORD = os.environ["RDS_PASSWORD"]
        HOST = os.environ["RDS_HOSTNAME"]
        PORT = os.environ["RDS_PORT"]

        database_url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
    else:
        # Ensure the instance folder exists
        INSTANCE_PATH = os.environ.get("INSTANCE_PATH") or Path.cwd() / "instance"
        INSTANCE_PATH.mkdir(exist_ok=True)

        database_url = f"sqlite:///{INSTANCE_PATH}/{FLASK_APP}.sqlite"

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OAuth Config
    FACEBOOK_OAUTH_CLIENT_ID = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
    FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")

    # Sendgrid Config
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    CONTACT_EMAIL = "berubejd@gmail.com"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
