import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import json
import pandas as pd


def find_elements_by_given_filter(container, class_name, filter_by):
    return container.find_elements(filter_by, class_name)


def find_element_by_given_filter(container, class_name, filter_by):
    return container.find_element(filter_by, class_name)


def extract_articles_data(driver_instance, articles_data):
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
            'article_date': article_date.text,
            'article_tag': article_tag.text
        }
    return driver_instance, articles_data


def extract_events_data(driver_instance, events_data):
    containers = find_elements_by_given_filter(driver_instance, ".card", By.CSS_SELECTOR)
    for container in containers:
        event_img = find_element_by_given_filter(container, ".card_photo div a img", By.CSS_SELECTOR)
        event_instance = find_element_by_given_filter(container, ".card_content-title", By.CSS_SELECTOR)
        event_link = find_element_by_given_filter(event_instance, "a", By.CSS_SELECTOR)
        event_name = find_element_by_given_filter(event_instance, "a span", By.CSS_SELECTOR)
        event_body = find_elements_by_given_filter(container, ".card_content div", By.CSS_SELECTOR)
        event_type = find_element_by_given_filter(container, ".card_footer a", By.CSS_SELECTOR)
        for event_data in event_body:
            try:
                event_date = event_data.text
            except NoSuchElementException as E:
                event_date = ''
            try:
                event_location = find_element_by_given_filter(event_data, "a span", By.CSS_SELECTOR).text
            except NoSuchElementException as E:
                event_location = ''
        events_data[event_name.text] = {
            'image_link': event_img.get_attribute('src'),
            'event_name': event_name.text,
            'event_link': event_link.get_attribute('href'),
            'event_type': event_type.text,
            'event_date': event_date,
            'event_location': event_location
        }
    return driver_instance, events_data


def list_activities(driver_instance, activities_data):
    elements = find_elements_by_given_filter(driver_instance, "container__09f24__YTiCU", By.CLASS_NAME)
    for element_val in elements:
        activity_by = find_element_by_given_filter(element_val, ".user-passport-info span a", By.CSS_SELECTOR)
        activity = find_element_by_given_filter(element_val, "link__09f24__nEC8H", By.CLASS_NAME)
        activity_name = activity.text
        activity_link = activity.get_attribute('href')
        if activity_name != '' and activity_name not in activities_data:
            activity_details = {
                'name': activity_name,
                'link': activity_link,
                'author': activity_by.text
            }
            activities_data[activity_name] = activity_details
    return driver_instance, activities_data


def json_to_csv(json_data, csv_file):
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

# Example usage
