import re
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy.exc import IntegrityError
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains

from yelp_project import logger_instance
from yelp_project.yelp_scrap.constants import (ARTICLES_URL, CHROME_EXECUTABLE_PATH, EVENTS_URL, ACTIVITIES_URL,
                                               EMAILS_CONSTANT, EMAIL_REGEX)
from yelp_project.yelp_scrap.models import Product, Category, Emails
from yelp_project.yelp_scrap.utils import (extract_articles_data, extract_events_data, list_activities,
                                           find_elements_by_given_filter,
                                           find_element_by_given_filter, DBActions)
from selenium.webdriver.support import expected_conditions as EC


class DriverClass:
    """
    Class to create chrome driver and related tasks
    """

    def __init__(self):
        options = ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        self.response_data = {}
        try:
            self.driver = Chrome(executable_path=CHROME_EXECUTABLE_PATH, options=options)
        except Exception as E:
            logger_instance.logger.exception('Chrome driver creation failure!!')

    def navigate_to_url(self, url):
        try:
            self.driver.get(url)
        except Exception as E:
            logger_instance.logger.exception('Driver not found!')

    def click_and_open_new_tab(self, link):
        try:
            action_chains = ActionChains(self.driver)
            action_chains.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            logger_instance.logger.info('New tab opened successfully!')
        except Exception as E:
            logger_instance.logger.exception('Error occurred in opening new tab!')

    def hover_element(self, element):
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            logger_instance.logger.info('New tab opened successfully!')
        except Exception as E:
            logger_instance.logger.exception('Error occurred in hovering element!')

    def return_to_tab_0(self):
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
            logger_instance.logger.info('Returned to tab 0 successfully!')
        except Exception as E:
            logger_instance.logger.exception('Error occurred shifting tab!')

    def quit_driver(self):
        self.driver.quit()
        logger_instance.logger.exception('Driver quit successfully!')


class ExtractArticlesClass(DriverClass):
    def extract_articles(self):
        self.navigate_to_url(ARTICLES_URL)

        more_articles = find_elements_by_given_filter(self.driver, "b-content-loop--layout_row", By.CLASS_NAME)
        for article in more_articles:
            link = find_elements_by_given_filter(article, "c-content-block__cta-link", By.CLASS_NAME)[0]
            self.click_and_open_new_tab(link)
            self.driver, self.response_data = extract_articles_data(self.driver, self.response_data)
            self.return_to_tab_0()
        self.quit_driver()
        return self.response_data


class ExtractEventsClass(DriverClass):
    def extract_events(self):
        self.navigate_to_url(EVENTS_URL)
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
        self.navigate_to_url(ACTIVITIES_URL)
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
    def extract_products(self):
        logger_instance.logger.info('Chrome driver created successfully!!')
        self.navigate_to_url(ACTIVITIES_URL)
        logger_instance.logger.info('Driver received page successfully!!')
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-link_anchor__09f24__eCD4u")))
        elements = find_elements_by_given_filter(self.driver, "header-link_anchor__09f24__eCD4u", By.CLASS_NAME)
        for element in elements:
            self.hover_element(element)
            product = element.text
            try:
                product_instance = Product(product_name=product)
                db_instance = DBActions()
                db_instance.add_to_db(product_instance)
                product_id = product_instance.product_id
            except IntegrityError as E:
                logger_instance.logger.exception(f'{product} already exists!')
            except Exception as E:
                logger_instance.logger.exception('Exception raised while adding data to database')

            hovered_element = find_element_by_given_filter(self.driver, "menu", By.TAG_NAME)
            products_list = []
            categories = find_elements_by_given_filter(hovered_element, "span", By.TAG_NAME)
            for i in categories:
                category = i.text
                if category != '':
                    products_list.append(category)
                    try:
                        category_instance = Category(category_name=category, product_id=product_id)
                        category_db = DBActions()
                        category_db.add_to_db(category_instance)
                    except IntegrityError as E:
                        logger_instance.logger.exception(f'{category} already exists!')
                    except AttributeError as E:
                        logger_instance.logger.exception('Attribute Error')
            self.response_data[product] = products_list
        self.quit_driver()
        return self.response_data


class ExtractEmailsClass(DriverClass):
    email_list = []

    def extract_emails(self):
        self.navigate_to_url(ACTIVITIES_URL)
        wait = WebDriverWait(self.driver, 10)
        links = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "a")))

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
