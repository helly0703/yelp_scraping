from flask import jsonify

from yelp_project import logger_instance
from yelp_project.yelp_scrap.constants import DATA_RECEIVED, EMAILS_CONSTANT
from yelp_project.yelp_scrap.driver import (ExtractProductsClass, ExtractActivitiesClass, ExtractEventsClass,
                                            ExtractArticlesClass, ExtractEmailsClass)


def extract_restaurants_list():
    """
    Jobs function to extract restaurants list
    """
    logger_instance.logger.warning('Restaurants Scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_restaurants_page()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})


def extract_restaurant_details():
    """
    Jobs function to extract restaurants details
    """
    logger_instance.logger.warning('Restaurants details scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_business_detail_page('restaurants')
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'message': data_to_display})


def extract_home_services_list():
    """
    Jobs function to extract home service list
    """
    logger_instance.logger.warning('Home Services list scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_home_services_page()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})


def extract_home_services_details():
    """
    Jobs function to extract home service details
    """
    logger_instance.logger.warning('Home Services details scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_business_detail_page('home services')
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'message': data_to_display})


def extract_auto_services_list():
    """
    Jobs function to extract auto service list
    """
    logger_instance.logger.warning('Auto Services list scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_auto_services_page()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})


def extract_auto_services_details():
    """
    Jobs function to extract auto service details
    """
    logger_instance.logger.warning('Auto Services detail scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_business_detail_page('auto services')
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'message': data_to_display})


def extract_other_services_list():
    """
    Jobs function to extract other service list
    """
    logger_instance.logger.warning('Other service list scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_other_services_page()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})


def extract_other_services_details():
    """
    Jobs function to extract other service details
    """
    logger_instance.logger.warning('Other service details scrapping api has been hit')
    products = ExtractProductsClass()
    data_to_display = products.extract_business_detail_page('other')
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'message': data_to_display})


def extract_categories():
    """
    Jobs function to extract categories
    """
    products = ExtractProductsClass()
    data_to_display = products.extract_categories()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})


def extract_recent_activities():
    """
    Jobs function to extract recent activities
    """
    activities = ExtractActivitiesClass()
    data_to_display = activities.extract_articles()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})


def extract_events():
    """
    Jobs function to extract events
    """
    events = ExtractEventsClass()
    data_to_display = events.extract_events()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})


def extract_articles():
    """
    Jobs function to extract articles
    """
    articles = ExtractArticlesClass()
    data_to_display = articles.extract_articles()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})


def extract_emails():
    """
    Jobs function to extract emails
    """
    emails = ExtractEmailsClass()
    data_to_display = emails.extract_emails()
    logger_instance.logger.info(DATA_RECEIVED)
    return jsonify({'data': data_to_display})
