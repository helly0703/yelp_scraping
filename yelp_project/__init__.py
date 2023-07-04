from datetime import datetime

from flask import Flask
from flask_apscheduler import APScheduler

from flask_sqlalchemy import SQLAlchemy


from yelp_project.yelp_scrap.custom_logger import CustomLoggerClass
logger_instance = CustomLoggerClass()

# Created SQLAlchemy Object
db = SQLAlchemy()
scheduler = APScheduler()


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
    # db.init_app(app)  # SQLAlchemy
    # scheduler.init_app(app)

    with app.app_context():
        from yelp_project.yelp_scrap.config import Config
        app.config.from_object(Config)
        db.init_app(app)  # SQLAlchemy
        scheduler.init_app(app)
        from yelp_project.yelp_scrap.routes import yelp_bp
        from yelp_project.yelp_scrap.jobs import (extract_restaurants_list, extract_restaurant_details,
                                                  extract_home_services_list, extract_home_services_details,
                                                  extract_auto_services_list, extract_auto_services_details,
                                                  extract_other_services_list, extract_other_services_details,
                                                  extract_categories, extract_recent_activities, extract_events,
                                                  extract_articles, extract_emails)
        app.register_blueprint(yelp_bp, url_prefix='/yelp')

        scheduler.add_job(id='restaurants-list', func=extract_restaurants_list, trigger='cron', day=1, hour=14, minute=36)
        scheduler.add_job(id='restaurants-details', func=extract_restaurant_details, trigger='cron', day=2, hour=14,
                          minute=36)
        scheduler.add_job(id='home-services-list', func=extract_home_services_list, trigger='cron', day=3, hour=14,
                          minute=36)
        scheduler.add_job(id='home-services-details', func=extract_home_services_details, trigger='cron', day=4, hour=14,
                          minute=50)
        scheduler.add_job(id='auto-services-list', func=extract_auto_services_list, trigger='cron', day=5, hour=14,
                          minute=36)
        scheduler.add_job(id='auto-services-details', func=extract_auto_services_details, trigger='cron', day=6, hour=14,
                          minute=36)
        scheduler.add_job(id='other-services-list', func=extract_other_services_list, trigger='cron', day=7, hour=14,
                          minute=36)
        scheduler.add_job(id='other-services-details', func=extract_other_services_details, trigger='cron', day=8, hour=14,
                          minute=36)
        scheduler.add_job(id='categories', func=extract_categories, trigger='cron', day=9, hour=14, minute=36)
        scheduler.add_job(id='recent-activities', func=extract_recent_activities, trigger='cron', day=10, hour=14,
                          minute=36)
        scheduler.add_job(id='events', func=extract_events, trigger='cron', day=11, hour=14, minute=36)
        scheduler.add_job(id='articles', func=extract_articles, trigger='cron', day=12, hour=14, minute=36)
        scheduler.add_job(id='emails', func=extract_emails, trigger='cron', day=13, hour=14, minute=36)
        scheduler.start()
        logger_instance.logger.info('Flask app object created successfully!')
    return app
