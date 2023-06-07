import logging

from flask import Blueprint, jsonify

from yelp_project import logger_instance
from yelp_project.yelp_scrap.constants import (PRODUCTS_CSV_FILE, ACTIVITIES_CSV, EVENTS_CSV, ARTICLES_CSV,
                                               EMAILS_CONSTANT, EMAILS_CSV, NO_EMAILS_FOUND)
from yelp_project.yelp_scrap.driver import (ExtractProductsClass, ExtractActivitiesClass, ExtractEventsClass,
                                            ExtractArticlesClass, ExtractEmailsClass)
from yelp_project.yelp_scrap.utils import json_to_csv, dict_to_csv

yelp_bp = Blueprint('yelp_bp', __name__)


@yelp_bp.route('/products', methods=['GET'])
def get_products():
    logger_instance.logger.warning('Products Scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_products()
    return jsonify({'products': data_to_display})


@yelp_bp.route('/products/download-csv', methods=['GET'])
def get_products_csv():
    products = ExtractProductsClass()
    data_to_display = products.extract_products()
    json_to_csv(data_to_display, PRODUCTS_CSV_FILE)
    return jsonify({'products': data_to_display})


@yelp_bp.route('/recent-activities', methods=['GET'])
def get_recent_activities():
    activities = ExtractActivitiesClass()
    data_to_display = activities.extract_articles()
    return jsonify({'activities': data_to_display})


@yelp_bp.route('/recent-activities/download-csv', methods=['GET'])
def get_recent_activities_csv():
    activities = ExtractActivitiesClass()
    data_to_display = activities.extract_articles()
    dict_to_csv(data_to_display, ACTIVITIES_CSV)
    return jsonify({'activities': data_to_display})


@yelp_bp.route('/events', methods=['GET'])
def get_events():
    events = ExtractEventsClass()
    data_to_display = events.extract_events()
    return jsonify({'events': data_to_display})


@yelp_bp.route('/events/download-csv', methods=['GET'])
def get_events_csv():
    events = ExtractEventsClass()
    data_to_display = events.extract_events()
    dict_to_csv(data_to_display, EVENTS_CSV)
    return jsonify({'events': data_to_display})


@yelp_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = ExtractArticlesClass()
    data_to_display = articles.extract_articles()
    return jsonify({'articles': data_to_display})


@yelp_bp.route('/articles/download-csv', methods=['GET'])
def get_articles_csv():
    articles = ExtractArticlesClass()
    data_to_display = articles.extract_articles()
    dict_to_csv(data_to_display, ARTICLES_CSV)
    return jsonify({'articles': data_to_display})


@yelp_bp.route('/emails', methods=['GET'])
def get_emails():
    emails = ExtractEmailsClass()
    data_to_display = emails.extract_emails()
    return jsonify({EMAILS_CONSTANT: data_to_display})


@yelp_bp.route('/emails/download-csv', methods=['GET'])
def get_emails_csv():
    emails = ExtractEmailsClass()
    data_to_display = emails.extract_emails()
    if data_to_display[EMAILS_CONSTANT]:
        dict_to_csv(data_to_display, EMAILS_CSV)
    else:
        data_to_display = NO_EMAILS_FOUND
    return jsonify({EMAILS_CONSTANT: data_to_display})
