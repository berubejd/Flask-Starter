# Flask Starter Template

This is a template that implements the basics of a Flask app utilizing the [factory pattern](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/).

For database access, this project also includes:

- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PyMySQL](https://pymysql.readthedocs.io/en/latest/)

In order to provide social login functionality (OAuth), the project utilizes [Flask-Dance](https://flask-dance.readthedocs.io/en/latest/) and incorporates a lot of the work provided in their [multi-provider example](https://github.com/singingwolfboy/flask-dance-multi-provider).

Although this example allows for the use of Facebook and Google logins, Flask-Dance offers a healthy list of blueprints and the ability to create custom blueprints, as well.

Email delivery is provided for via SendGrid and currently integrated with the contact form only.

The simple layout utilizes [Bootstrap 4](https://getbootstrap.com/) and borrows from the [Cover](https://getbootstrap.com/docs/4.4/examples/cover/) example.

## Screenshot

### Landing page
![Landing Screenshot](images/landing.png?raw-true)

### Account login and information
![Login Screenshot](images/login.png?raw-true)
![Account Info Screenshot](images/accountinfo.png?raw-true)

## Configuration

Most of the configuration is handled in [config.py](https://github.com/berubejd/Flask-Starter/blob/master/config.py).  While there are a number of defaults, many of them are meant to be overridden in the environment.  At a minimum, you will probably want to set:

- FLASK_APP = name (This should match what the 'application' directory is renamed to.)
- FLASK_ENV = development (If you would like the app to provide log output and autoreload.)

Access to provider's OAuth services will also require the appropriate client id and secrets to be set.  Additionally, a SendGrid API key will also be required in the environment for contact emails to operate.

Finally, in order for callbacks to complete, the server needs to be utilizing TLS.  Flask can be started with the following command in order to create temporary certificates:  ```flask run --cert=adhoc```