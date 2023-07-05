import datetime

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from sqlalchemy.exc import IntegrityError

from yelp_project import db, logger_instance


class DBActions:
    def add_to_db(self, data_instance):
        db.session.add(data_instance)
        self.commit_session()

    def commit_session(self):
        db.session.commit()

    def check_if_data_exists(self, table_name, key_name, value):
        product_id = db.session.query(table_name).filter_by(**{key_name: value}).first()
        return product_id

    def insert_into_mapping_table(self, insert_data):
        result = db.session.execute(insert_data)
        return result

    def get_data(self, table_name,filter_params):
        products = db.session.query(table_name).filter_by(**filter_params)
        return products


def convert_str_to_date(string_date):
    """
    Convert string to date
    """
    try:
        date_format = "%B %d, %Y"
        date_object = datetime.datetime.strptime(string_date, date_format).date()
        return date_object
    except ValueError:
        return None


def find_elements_by_given_filter(container, class_name, filter_by):
    """
    Selenium function to find elements based on filter
    """
    return container.find_elements(filter_by, class_name)


def find_element_by_given_filter(container, class_name, filter_by):
    """
    Selenium function to find element based on filter
    """
    try:
        if container is not None:
            return container.find_element(filter_by, class_name)
    except NoSuchElementException:
        return None


def extract_articles_data(driver_instance, articles_data):
    """
    Extract articles data
    """
    logger_instance.logger.info('Started fetching articles!')
    containers = find_elements_by_given_filter(driver_instance, ".c-card--has-image", By.CSS_SELECTOR)
    for container in containers:
        article_link = find_element_by_given_filter(container, ".c-card__media .c-card__link", By.CSS_SELECTOR)
        article_image = find_element_by_given_filter(container, ".c-card__media .c-card__image img", By.CSS_SELECTOR)
        article_content = find_element_by_given_filter(container, ".c-card__content", By.CSS_SELECTOR)
        article_tag = find_element_by_given_filter(article_content, ".t-tag", By.CSS_SELECTOR)
        article_title = find_element_by_given_filter(article_content, ".c-card__title", By.CSS_SELECTOR)
        article_date = find_element_by_given_filter(article_content, ".c-card__date", By.CSS_SELECTOR)
        articles_data[article_title.text] = {
            'article_title': article_title.text,
            'article_image': article_image.get_attribute('src'),
            'article_link': article_link.get_attribute('href'),
            'article_date': convert_str_to_date(article_date.text),
            'article_tag': article_tag.text
        }
        try:
            from yelp_project.yelp_scrap.models import Article
            article_instance = Article(**articles_data[article_title.text])
            article_db = DBActions()
            article_id = article_db.check_if_data_exists(Article, 'article_title', article_title.text)
            if not article_id:
                article_db.add_to_db(article_instance)
        except IntegrityError as E:
            logger_instance.logger.exception(f'{article_title.text} already exists!')
    logger_instance.logger.info('Finished fetching articles and storing in database!')
    return driver_instance, articles_data


def extract_events_data(driver_instance, events_data):
    """
    Extract event data
    """
    logger_instance.logger.info('Started fetching events!')

    containers = find_elements_by_given_filter(driver_instance, ".card", By.CSS_SELECTOR)
    for container in containers:
        event_img = find_element_by_given_filter(container, ".card_photo div a img", By.CSS_SELECTOR)
        event_instance = find_element_by_given_filter(container, ".card_content-title", By.CSS_SELECTOR)
        event_link = find_element_by_given_filter(event_instance, "a", By.CSS_SELECTOR)
        event_name = find_element_by_given_filter(event_instance, "a span", By.CSS_SELECTOR)
        event_body = find_elements_by_given_filter(container, ".card_content div", By.CSS_SELECTOR)
        event_type = find_element_by_given_filter(container, ".card_footer a", By.CSS_SELECTOR)
        event_date = event_body[0].text
        event_location = event_body[1].text
        events_data[event_name.text] = {
            'image_link': event_img.get_attribute('src'),
            'event_name': event_name.text,
            'event_link': event_link.get_attribute('href'),
            'event_type': event_type.text,
            'event_date': convert_str_to_date(event_date),
            'event_location': event_location
        }
        try:
            from yelp_project.yelp_scrap.models import Event
            event_instance = Event(**events_data[event_name.text])
            event_db = DBActions()
            event_db.add_to_db(event_instance)
        except IntegrityError as E:
            logger_instance.logger.info(f'{event_name.text} already exists!')
        except Exception as E:
            logger_instance.logger.exception('Exception raised while adding data to database!')
    logger_instance.logger.info('Completed fetching events!')
    return driver_instance, events_data


def list_activities(driver_instance, activities_data):
    """
    Extract activities data
    """
    logger_instance.logger.info('Started fetching activities!')

    elements = find_elements_by_given_filter(driver_instance, "container__09f24__YTiCU", By.CLASS_NAME)
    for element_val in elements:
        activity_type = 'Unknown'
        ratings = 0
        activity_by = find_element_by_given_filter(element_val, ".user-passport-info span a", By.CSS_SELECTOR)
        activity = find_element_by_given_filter(element_val, "link__09f24__nEC8H", By.CLASS_NAME)
        activity_name = activity.text
        activity_link = activity.get_attribute('href')
        try:
            if rating := find_element_by_given_filter(
                    element_val, "five-stars__09f24__mBKym", By.CLASS_NAME
            ):
                activity_type = 'Review'
                ratings = float(rating.get_attribute(
                    'aria-label').split()[0]) if rating is not None else 0
        except Exception:
            activity_type = 'Post'
            ratings = 0

        if activity_name != '' and activity_name not in activities_data:
            activities_data[activity_name] = {
                'business': activity_name,
                'business_link': activity_link,
                'activity_author': activity_by.text,
                'activity_type': activity_type,
                'business_rating': ratings,
            }
            try:
                from yelp_project.yelp_scrap.models import Activities
                activity_instance = Activities(**activities_data[activity_name])
                if len(activity_instance.filter_by_values(activity_by.text, activity_name, activity_type)) > 0:
                    logger_instance.logger.info(
                        f'{activity_type} by {activity_by.text} for {activity_name} already exists!')
                else:
                    activity_db = DBActions()
                    activity_db.add_to_db(activity_instance)
                    activity_db.commit_session()
            except IntegrityError as E:
                logger_instance.logger.info(f'{activity_name} already exists!')
            except Exception as E:
                logger_instance.logger.exception('Exception raised while adding data to database!')
    logger_instance.logger.info('Finished fetching activities and storing it to database!')

    return driver_instance, activities_data


def json_to_csv(json_data, csv_file):
    """
    Store dictionary data to csv
    """
    df = pd.DataFrame.from_dict(json_data)
    df.to_csv(csv_file, index=False)


def dict_to_csv(data_dict, csv_file):
    # Convert the dictionary to a pandas DataFrame
    dict_list = [{**{'srno': index + 1}, **value} for index, value in enumerate(data_dict.values())]

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(dict_list)

    # Set the 'srno' column as the index
    df.set_index('srno', inplace=True)

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file)


def get_proxies():
    with open('/media/root357/Data/Yelp/yelp_scraping/yelp_project/yelp_scrap/list_proxy.txt', 'r') as file:
        proxies = file.readlines()
    return proxies
