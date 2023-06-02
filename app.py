from flask import Flask, jsonify

from articles_selenium import get_articles_data
from emails_selenium import get_email_data
from events_selenium import get_events_data
from products_selenium import get_products_data
from recent_activities_selenium import get_recent_activities_data

app = Flask(__name__)


@app.route('/products', methods=['GET'])
def get_products():
    data = get_products_data()
    return jsonify({'products_data': data})


@app.route('/recent-activities', methods=['GET'])
def get_recent_activities():
    data = get_recent_activities_data()
    return jsonify({'recent-activities': data})


@app.route('/events', methods=['GET'])
def get_events():
    data = get_events_data()
    return jsonify({'events': data})


@app.route('/articles', methods=['GET'])
def get_articles():
    data = get_articles_data()
    return jsonify({'articles': data})


@app.route('/emails', methods=['GET'])
def get_emails():
    data = get_email_data()
    return jsonify({'emails': data})


if __name__ == '__main__':
    app.run()
