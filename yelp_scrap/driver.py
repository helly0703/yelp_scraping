import re
import time

from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains

from yelp_scrap.constants import (ARTICLES_URL, CHROME_EXECUTABLE_PATH, EVENTS_URL, ACTIVITIES_URL,
                                  EMAILS_CONSTANT, EMAIL_REGEX)
from yelp_scrap.utils import (extract_articles_data, extract_events_data, list_activities,
                              find_elements_by_given_filter,
                              find_element_by_given_filter)
from selenium.webdriver.support import expected_conditions as EC


class DriverClass:
    """
    Class to create chrome driver and related tasks
    """

    def __init__(self):
        options = ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        self.response_data = {}
        self.driver = Chrome(executable_path=CHROME_EXECUTABLE_PATH, options=options)
        time.sleep(2)

    def navigate_to_url(self, url):
        self.driver.get(url)

    def click_and_open_new_tab(self, link):
        action_chains = ActionChains(self.driver)
        action_chains.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def hover_element(self, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def return_to_tab_0(self):
        self.driver.switch_to.window(self.driver.window_handles[0])

    def quit_driver(self):
        self.driver.quit()


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
        self.navigate_to_url(ACTIVITIES_URL)
        time.sleep(2)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-link_anchor__09f24__eCD4u")))
        elements = find_elements_by_given_filter(self.driver, "header-link_anchor__09f24__eCD4u", By.CLASS_NAME)
        for element in elements:
            self.hover_element(element)
            product = element.text
            hovered_element = find_element_by_given_filter(self.driver, "menu", By.TAG_NAME)
            products_list = []
            categories = find_elements_by_given_filter(hovered_element, "span", By.TAG_NAME)
            for i in categories:
                category = i.text
                if category != '':
                    products_list.append(category)
            self.response_data[product] = products_list
        self.quit_driver()
        return self.response_data


class ExtractEmailsClass(DriverClass):
    email_list = []

    def extract_emails(self):
        self.navigate_to_url(ACTIVITIES_URL)
        time.sleep(2)
        links = find_elements_by_given_filter(self.driver, "a", By.TAG_NAME)
        email_pattern = re.compile(EMAIL_REGEX)

        for link in links:
            if href := link.get_attribute('href'):
                if email_matches := email_pattern.findall(href):
                    for email in email_matches:
                        self.email_list.append(email)
        self.driver.quit()
        self.response_data = {EMAILS_CONSTANT: self.email_list}
        return self.response_data
