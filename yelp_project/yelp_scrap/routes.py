from flask import Blueprint

from yelp_project.yelp_scrap.jobs import (extract_restaurants_list, extract_restaurant_details,
                                          extract_home_services_list, extract_home_services_details,
                                          extract_auto_services_list, extract_auto_services_details,
                                          extract_other_services_list, extract_other_services_details,
                                          extract_categories, extract_recent_activities, extract_events,
                                          extract_articles, extract_emails)

yelp_bp = Blueprint('yelp_bp', __name__)


@yelp_bp.route('/restaurants/listings', methods=['GET'])
def get_restaurant_listings():
    return extract_restaurants_list()


@yelp_bp.route('/restaurants/details', methods=['GET'])
def get_restaurant_details():
    return extract_restaurant_details()


@yelp_bp.route('/homeservices/listings', methods=['GET'])
def get_home_services_listings():
    return extract_home_services_list()


@yelp_bp.route('/homeservices/details', methods=['GET'])
def get_home_services_details():
    return extract_home_services_details()


@yelp_bp.route('/autoservices/listings', methods=['GET'])
def get_auto_services_listings():
    return extract_auto_services_list()


@yelp_bp.route('/autoservices/details', methods=['GET'])
def get_auto_services_details():
    return extract_auto_services_details()


@yelp_bp.route('/others/listings', methods=['GET'])
def get_other_services_listings():
    return extract_other_services_list()


@yelp_bp.route('/others/details', methods=['GET'])
def get_other_services_details():
    return extract_other_services_details()


@yelp_bp.route('/categories', methods=['GET'])
def get_categories_list():
    return extract_categories()


@yelp_bp.route('/recent-activities', methods=['GET'])
def get_recent_activities():
    return extract_recent_activities()


@yelp_bp.route('/events', methods=['GET'])
def get_events():
    return extract_events()


@yelp_bp.route('/articles', methods=['GET'])
def get_articles():
    return extract_articles()


@yelp_bp.route('/emails', methods=['GET'])
def get_emails():
    return extract_emails()
