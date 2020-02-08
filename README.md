# Flask Starter Template

This is a template that implements the basics of a Flask app utilizing the [factory pattern](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/).

For database access, this project also includes:

- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PyMySQL](https://pymysql.readthedocs.io/en/latest/)

The simple layout utilizes [Bootstrap 4](https://getbootstrap.com/) and borrows from the [Cover](https://getbootstrap.com/docs/4.4/examples/cover/) example.

## Configuration

Most of the configuration is handled in [config.py](https://github.com/berubejd/Flask-Starter/blob/master/config.py).  While there are a number of defaults, many of them are meant to be overridden in the environment.  At a minimum, you will probably want to set:

- FLASK_APP = name (This should match what the 'application' directory is renamed to.)
- FLASK_ENV = development (If you would like the app to provide log output and autoreload.)