import re

from selenium.common import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy.exc import IntegrityError
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from yelp_project import logger_instance
from yelp_project.yelp_scrap.constants import (ARTICLES_URL, CHROME_EXECUTABLE_PATH, EVENTS_URL, ACTIVITIES_URL,
                                               EMAILS_CONSTANT, EMAIL_REGEX, DRIVER_CREATION_FAILURE, PAGE_RECEIVED,
                                               PAGE_NOT_FOUND, TAB_OPENED, ERROR_IN_NEW_TAB, ELEMENT_HOVERED,
                                               ERROR_IN_HOVERING, RETURNED_TO_TAB, ERROR_SHIFTING_TAB, DRIVER_QUIT,
                                               STATUS_CODE, MSG, CONNECTION_INTERRUPTED)
from yelp_project.yelp_scrap.models import Business, Category, Emails, Feature, business_categories
from yelp_project.yelp_scrap.utils import (extract_articles_data, extract_events_data, list_activities,
                                           find_elements_by_given_filter,
                                           find_element_by_given_filter, DBActions)
from selenium.webdriver.support import expected_conditions as EC


class DriverClass:
    """
    Class to create chrome driver and related tasks using selenium
    """

    def __init__(self):
        # PROXY = "167.249.29.218:999"  # IP:PORT or HOST:PORT
        #
        # """initialize driver"""
        options = ChromeOptions()
        #
        # # options.add_argument('--headless')  # Run Chrome in headless mode
        # options.add_argument('--proxy-server=%s' % PROXY)  # Run Chrome in headless mode
        self.response_data = {}
        try:
            self.driver = Chrome(executable_path=CHROME_EXECUTABLE_PATH, options=options)
        except Exception as E:
            logger_instance.logger.exception(DRIVER_CREATION_FAILURE)

    def navigate_to_url(self, url):
        """Navigate to the url"""
        try:
            self.driver.get(url)
            logger_instance.logger.info(PAGE_RECEIVED)
        except Exception as E:
            logger_instance.logger.exception(PAGE_NOT_FOUND)
            return Exception

    def click_and_open_new_tab(self, link):
        """Click element and open url in new tab"""
        try:
            action_chains = ActionChains(self.driver)
            action_chains.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger_instance.logger.info(TAB_OPENED)
        except Exception as E:
            logger_instance.logger.exception(ERROR_IN_NEW_TAB)

    def hover_element(self, element):
        """Hover element"""
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            logger_instance.logger.info(ELEMENT_HOVERED)
        except Exception as E:
            logger_instance.logger.exception(ERROR_IN_HOVERING)

    def return_to_tab_0(self):
        """Return to the tab zero in chrome"""
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
            logger_instance.logger.info(RETURNED_TO_TAB)
        except Exception as E:
            logger_instance.logger.exception(ERROR_SHIFTING_TAB)

    def click_escape(self):
        action_chains = ActionChains(self.driver)
        action_chains.send_keys(Keys.ESCAPE)
        action_chains.perform()

    def quit_driver(self):
        """To quit driver"""
        self.driver.quit()
        logger_instance.logger.info(DRIVER_QUIT)


class ExtractArticlesClass(DriverClass):
    def extract_articles(self):
        """
            Start extraction of articles by fetching page from url, goes to next
             page if required, make clicks and other stuff
         """
        if self.navigate_to_url(ARTICLES_URL) is not None:
            return {STATUS_CODE: 400, MSG: CONNECTION_INTERRUPTED}
        more_articles = find_elements_by_given_filter(self.driver, "b-content-loop--layout_row", By.CLASS_NAME)
        logger_instance.logger.info('More Articles fetched Successfully!')
        for article in more_articles:
            link = find_elements_by_given_filter(article, "c-content-block__cta-link", By.CLASS_NAME)[0]
            self.click_and_open_new_tab(link)
            self.driver, self.response_data = extract_articles_data(self.driver, self.response_data)
            self.return_to_tab_0()
        self.quit_driver()
        return self.response_data


class ExtractEventsClass(DriverClass):
    """Inherits driver class"""

    def extract_events(self):
        """
            Start extraction of events by fetching page from url, goes to next
             page if required, make clicks and other stuff
         """
        if self.navigate_to_url(EVENTS_URL) is not None:
            return {STATUS_CODE: 400, MSG: CONNECTION_INTERRUPTED}
        more_events = find_element_by_given_filter(self.driver, ".va-grid div a", By.CSS_SELECTOR)
        self.click_and_open_new_tab(more_events)
        self.driver, self.response_data = extract_events_data(self.driver, self.response_data)
        while len(find_elements_by_given_filter(self.driver, ".arrange_unit .next", By.CSS_SELECTOR)) > 0:
            next_element = find_element_by_given_filter(self.driver, ".arrange_unit .next", By.CSS_SELECTOR)
            self.click_and_open_new_tab(next_element)
            self.driver, self.response_data = extract_events_data(self.driver, self.response_data)
        self.quit_driver()
        return self.response_data


class ExtractActivitiesClass(DriverClass):
    def extract_articles(self):
        """
            Start extraction of activities by fetching page from url, goes to next
             page if required, make clicks and other stuff
         """
        if self.navigate_to_url(ACTIVITIES_URL) is not None:
            return {STATUS_CODE: 400, MSG: CONNECTION_INTERRUPTED}
        self.driver, self.response_data = list_activities(self.driver, self.response_data)
        while len(self.response_data) < 50:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            show_next_button = find_element_by_given_filter(self.driver, "//*[text()='Show more activity']",
                                                            By.XPATH)
            show_next_button.click()
            self.driver, self.response_data = list_activities(self.driver, self.response_data)
        self.quit_driver()
        return self.response_data


class ExtractProductsClass(DriverClass):
    links_for_more_categories = []

    @staticmethod
    def add_category_to_db(category_name):
        print(category_name)
        try:
            category_instance = Category(category_name=category_name)
            category_db = DBActions()
            category_id = category_db.check_if_data_exists(Category, 'category_name', category_name)

            if not category_id:
                category_db.add_to_db(category_instance)
            return category_id
        except IntegrityError as E:
            logger_instance.logger.exception(f'{category_name} already exists!')
        except AttributeError as E:
            logger_instance.logger.exception('Attribute Error')

    @staticmethod
    def add_feature_to_db(feature_name):
        try:
            feature_instance = Feature(category_name=feature_name)
            feature_db = DBActions()
            feature_id = feature_db.check_if_data_exists(Feature, 'feature_name', feature_name)
            if not feature_id:
                feature_db.add_to_db(feature_instance)
        except IntegrityError as E:
            logger_instance.logger.exception(f'{feature_name} already exists!')
        except AttributeError as E:
            logger_instance.logger.exception('Attribute Error')

    @staticmethod
    def add_restaurant_to_db(restaurant_data, business_type):
        print(restaurant_data)
        try:
            business_object = Business()
            business_id = business_object.add_business_to_db(restaurant_data, business_type)
            business_object.add_business_categories(restaurant_data['category_list'], business_id)
            business_object.add_business_features(restaurant_data['features_list'], business_id)
            business_object.add_business_highlights(restaurant_data['highlights_list'], business_id)

        except IntegrityError as E:
            logger_instance.logger.exception(f"{restaurant_data['restaurant_name']} already exists!")
        except AttributeError as E:
            logger_instance.logger.exception('Attribute Error')

    def extract_categories(self):
        """
            Start extraction of products by fetching page from url, goes to next
             page if required, make clicks and other stuff
         """
        if self.navigate_to_url(ACTIVITIES_URL) is not None:
            return {STATUS_CODE: 400, MSG: CONNECTION_INTERRUPTED}
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-link_anchor__09f24__eCD4u")))
        elements = find_elements_by_given_filter(self.driver, "header-link_anchor__09f24__eCD4u", By.CLASS_NAME)
        for element in elements:
            self.hover_element(element)
            menu = find_elements_by_given_filter(self.driver, "menu-item__09f24__GEQP6", By.CLASS_NAME)
            for i in menu:
                category = i.text
                if category != '':
                    self.add_category_to_db(category)
            if element.get_attribute('href'):
                self.click_and_open_new_tab(element)
                vertical_containers = find_elements_by_given_filter(self.driver, "verticalLayout__09f24__YrUSt",
                                                                    By.CLASS_NAME)
                for container in vertical_containers:
                    labels = find_elements_by_given_filter(container, 'padding-b1__09f24__mrxd5',
                                                           By.CLASS_NAME)
                    for label in labels:
                        if label.text == 'Category':
                            self.click_and_open_new_tab(find_element_by_given_filter(container, "a",
                                                                                     By.TAG_NAME))
                            modal_body = find_element_by_given_filter(self.driver, "modal__09f24__EJkd3",
                                                                      By.CLASS_NAME)
                            categories = find_elements_by_given_filter(modal_body, "css-qgunke", By.CLASS_NAME)
                            for category in categories:
                                self.add_category_to_db(category.text.lower())
                            self.click_escape()

                        elif label.text == 'Features':
                            self.click_and_open_new_tab(find_element_by_given_filter(container, "a",
                                                                                     By.TAG_NAME))
                            modal_body = find_element_by_given_filter(self.driver, "modal__09f24__EJkd3",
                                                                      By.CLASS_NAME)
                            features = find_elements_by_given_filter(modal_body, "li", By.TAG_NAME)
                            for feature in features:
                                feature_name = feature.text.lower()
                                if "offers" in feature_name:
                                    feature_name = feature_name.strip("offer").strip()
                                self.add_feature_to_db(feature_name)
                            self.click_escape()
            self.return_to_tab_0()

        self.response_data['Success'] = 'Data extracted successfully'
        self.quit_driver()
        return self.response_data

    def extract_restaurant_data(self):
        wait = WebDriverWait(self.driver, 40)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "container__09f24__mpR8_")))
        elements = find_elements_by_given_filter(self.driver, "container__09f24__mpR8_", By.CLASS_NAME)
        restaurant_data = {}
        for element in elements:
            restaurant_image_element = find_element_by_given_filter(element, "css-w8rns", By.CLASS_NAME)
            restaurant_image_element_link = find_element_by_given_filter(restaurant_image_element, "img", By.TAG_NAME)
            restaurant_data['restaurant_img_link'] = restaurant_image_element_link.get_attribute('src')
            restaurant_name_element = find_element_by_given_filter(element, "css-19v1rkv",
                                                                   By.CLASS_NAME)
            restaurant_data['restaurant_name'] = restaurant_name_element.text  # Restaurant name
            restaurant_data['restaurant_link_element'] = restaurant_name_element.get_attribute('href')  # Restaurant url
            ratings_element = find_element_by_given_filter(element, "five-stars--regular__09f24__DgBNj",
                                                           By.CLASS_NAME)
            restaurant_data['ratings'] = float(ratings_element.get_attribute(
                'aria-label').split()[0]) if ratings_element is not None else 0  # Ratings
            restaurant_data['category_list'] = [category.text for category in
                                                find_elements_by_given_filter(element, "css-11bijt4",
                                                                              By.CLASS_NAME)]  # Restaurant categories
            restaurant_data['highlights_list'] = [highlights.text for highlights in
                                                  find_elements_by_given_filter(element,
                                                                                "mobile-text-medium__09f24__MZ1v6",
                                                                                By.CLASS_NAME)]  # Restaurant highlights
            restaurant_data['features_list'] = [feature.text for feature in
                                                find_elements_by_given_filter(element, "css-1oibaro", By.CLASS_NAME)]
            if restaurant_data['restaurant_name'] != '':
                self.add_restaurant_to_db(restaurant_data, 'restaurants')

    def extract_restaurants_page(self):
        if self.navigate_to_url(ACTIVITIES_URL) is not None:
            return {STATUS_CODE: 400, MSG: CONNECTION_INTERRUPTED}
        wait = WebDriverWait(self.driver, 40)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-link_anchor__09f24__eCD4u")))
        elements = find_elements_by_given_filter(self.driver, "header-link_anchor__09f24__eCD4u", By.CLASS_NAME)

        self.click_and_open_new_tab(elements[0])
        self.extract_restaurant_data()
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pagination__09f24__VRjN4")))
        next_links = find_element_by_given_filter(self.driver, "pagination__09f24__VRjN4", By.CLASS_NAME)
        while (link_for_next_page := find_element_by_given_filter(next_links,
                                                                  "next-link",
                                                                  By.CLASS_NAME)) is not None:
            action_chains = ActionChains(self.driver)
            action_chains.key_down(Keys.CONTROL).click(link_for_next_page).key_up(Keys.CONTROL).perform()
            self.extract_restaurant_data()
        self.driver.quit()

    def extract_restaurant_detail_page(self):
        if self.navigate_to_url('https://www.yelp.com/biz/panera-bread-daly-city') is not None:
            return {STATUS_CODE: 400, MSG: CONNECTION_INTERRUPTED}
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//section[@aria-label='Menu']")))
        menu_main_section = find_element_by_given_filter(self.driver, "//section[@aria-label='Menu']", By.XPATH)
        menu_section = find_elements_by_given_filter(menu_main_section, "css-gnym5v", By.CLASS_NAME)
        for dishes in menu_section:
            dish = find_element_by_given_filter(dishes, "p", By.TAG_NAME)
            print(dish.text)

        wait.until(EC.visibility_of_element_located((By.XPATH, "//section[@aria-label='Menu']")))
        ammenities_section = find_element_by_given_filter(self.driver, "//section[@aria-label='Amenities and More']",
                                                          By.XPATH)
        more_ammenities = find_element_by_given_filter(ammenities_section, "css-1wayfxy", By.CLASS_NAME)
        if more_ammenities:
            action_chains = ActionChains(self.driver)
            action_chains.key_down(Keys.CONTROL).click(more_ammenities).key_up(Keys.CONTROL).perform()
            features_list_elements = find_elements_by_given_filter(ammenities_section, "css-1p9ibgf", By.CLASS_NAME)
            for feature in features_list_elements:
                print(feature.text)

        contact_div_element = find_element_by_given_filter(self.driver, "css-xp8w2v", By.CLASS_NAME)
        all_elements = find_elements_by_given_filter(contact_div_element, "css-1p9ibgf", By.CLASS_NAME)
        website_link = all_elements[0].text
        contact = all_elements[1].text
        location_element = find_element_by_given_filter(contact_div_element, "css-qyp8bo", By.CLASS_NAME)
        location = location_element.text

        self.driver.quit()


class ExtractEmailsClass(DriverClass):
    email_list = []

    def extract_emails(self):
        """
            Start extraction of emails by fetching page from url, goes to next
             page if required, make clicks and other stuff
         """
        if self.navigate_to_url(ACTIVITIES_URL) is not None:
            return {STATUS_CODE: 400, MSG: CONNECTION_INTERRUPTED}
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "a")))
        links = find_elements_by_given_filter(self.driver, "a", By.TAG_NAME)

        email_pattern = re.compile(EMAIL_REGEX)

        for link in links:
            if href := link.get_attribute('href'):
                if email_matches := email_pattern.findall(href):
                    for email in email_matches:
                        self.email_list.append(email)
                        try:
                            email_instance = Emails(email=email)
                            email_db = DBActions()
                            email_db.add_to_db(email_instance)
                        except IntegrityError as E:
                            logger_instance.logger.exception(f'{email} already exists!')
        self.driver.quit()
        self.response_data = {EMAILS_CONSTANT: self.email_list}
        return self.response_data
