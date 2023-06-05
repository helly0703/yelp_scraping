from flask import Flask, jsonify

from yelp_scrap.constants import EMAILS_CONSTANT, PRODUCTS_CSV_FILE, ARTICLES_CSV, ACTIVITIES_CSV, EMAILS_CSV, \
    EVENTS_CSV
from yelp_scrap.driver import (ExtractArticlesClass, ExtractEventsClass, ExtractActivitiesClass,
                               ExtractProductsClass, ExtractEmailsClass)
from yelp_scrap.utils import json_to_csv, dict_to_csv

app = Flask(__name__)


@app.route('/products', methods=['GET'])
def get_products():
    products = ExtractProductsClass()
    data_to_display = products.extract_products()
    json_to_csv(data_to_display, PRODUCTS_CSV_FILE)
    return jsonify({'products': data_to_display})


@app.route('/recent-activities', methods=['GET'])
def get_recent_activities():
    activities = ExtractActivitiesClass()
    data_to_display = activities.extract_articles()
    dict_to_csv(data_to_display, ACTIVITIES_CSV)
    return jsonify({'activities': data_to_display})


@app.route('/events', methods=['GET'])
def get_events():
    events = ExtractEventsClass()
    data_to_display = events.extract_events()
    dict_to_csv(data_to_display, EVENTS_CSV)
    return jsonify({'events': data_to_display})


@app.route('/articles', methods=['GET'])
def get_articles():
    articles = ExtractArticlesClass()
    data_to_display = articles.extract_articles()
    dict_to_csv(data_to_display, ARTICLES_CSV)
    return jsonify({'articles': data_to_display})


@app.route('/emails', methods=['GET'])
def get_emails():
    emails = ExtractEmailsClass()
    data_to_display = emails.extract_emails()
    dict_to_csv(data_to_display, EMAILS_CSV)
    return jsonify({EMAILS_CONSTANT: data_to_display})


if __name__ == '__main__':
    app.run()
