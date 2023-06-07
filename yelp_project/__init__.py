import logging

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from yelp_project.yelp_scrap.config import Config
from yelp_project.yelp_scrap.custom_logger import CustomLoggerClass

# Created SQLAlchemy Object
db = SQLAlchemy()

logger_instance = CustomLoggerClass()


def create_app():
    """
    Construct the core application.

    The whole function can be divided in 4 steps below

    >> Create a Flask app object, which derives configuration values (either from a Python class, a config file,
    or environment variables).
    >> Initialize plugins accessible to any part of our app, such as a database (via flask_sqlalchemy).
    >> Import the logic which makes up our app (such as routes).
    >> Register Blueprints.
    """
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(Config)
    db.init_app(app)  # SQLAlchemy

    from yelp_project.yelp_scrap.routes import yelp_bp
    from yelp_project.yelp_scrap import models
    app.register_blueprint(yelp_bp, url_prefix='/yelp')

    logger_instance.logger.info('Flask app object created successfully!')
    return app
