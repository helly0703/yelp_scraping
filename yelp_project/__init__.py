from flask import Flask

from yelp_project.yelp_scrap import routes


def create_app():
    """
    Construct the core application.

    The whole function can be divided in 4 steps below

    >> Create a Flask app object, which derives configuration values (either from a Python class, a config file,
    or environment variables).
    >> Initialize plugins accessible to any part of our app, such as a database (via flask_sqlalchemy),
    Redis (via flask_redis) or user authentication (via Flask-Login).
    >> Import the logic which makes up our app (such as routes).
    >> Register Blueprints.
    """
    app = Flask(__name__, instance_relative_config=False)
    app.register_blueprint(routes.yelp_bp, url_prefix='/yelp')
    return app
