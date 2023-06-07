import re
from selenium.webdriver.support.wait import WebDriverWait
from sqlalchemy.exc import IntegrityError
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains

from yelp_project import logger_instance
from yelp_project.yelp_scrap.constants import (ARTICLES_URL, CHROME_EXECUTABLE_PATH, EVENTS_URL, ACTIVITIES_URL,
                                               EMAILS_CONSTANT, EMAIL_REGEX, DRIVER_CREATION_FAILURE, PAGE_RECEIVED,
                                               PAGE_NOT_FOUND, TAB_OPENED, ERROR_IN_NEW_TAB, ELEMENT_HOVERED,
                                               ERROR_IN_HOVERING, RETURNED_TO_TAB, ERROR_SHIFTING_TAB, DRIVER_QUIT,
                                               STATUS_CODE, MSG, CONNECTION_INTERRUPTED)
from yelp_project.yelp_scrap.models import Product, Category, Emails
from yelp_project.yelp_scrap.utils import (extract_articles_data, extract_events_data, list_activities,
                                           find_elements_by_given_filter,
                                           find_element_by_given_filter, DBActions)
from selenium.webdriver.support import expected_conditions as EC


class DriverClass:
    """
    Class to create chrome driver and related tasks using selenium
    """

    def __init__(self):
        """initialize driver"""
        options = ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
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
    def extract_products(self):
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
            product = element.text
            hovered_element = find_element_by_given_filter(self.driver, "menu", By.TAG_NAME)
            categories = find_elements_by_given_filter(hovered_element, "span", By.TAG_NAME)
            try:
                product_instance = Product(product_name=product)
                db_instance = DBActions()
                product_id = db_instance.check_if_data_exists(Product, 'product_name', product)
                if not product_id:
                    db_instance.add_to_db(product_instance)
                    product_id = product_instance.product_id
            except IntegrityError as E:
                logger_instance.logger.exception(f'{product} already exists!')
            except Exception as E:
                logger_instance.logger.exception('Exception raised while adding data to database')
            products_list = []
            for i in categories:
                category = i.text
                if category != '':
                    products_list.append(category)
                    try:
                        category_instance = Category(category_name=category, product_id=product_id)
                        category_db = DBActions()
                        category_id = category_db.check_if_data_exists(Category, 'category_name', category)
                        if not category_id:
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
