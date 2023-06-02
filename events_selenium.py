import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

events_data = {}


def extract_events(driver_instance):
    containers = driver_instance.find_elements(By.CSS_SELECTOR, ".card")
    time.sleep(2)
    for container in containers:
        event_img = container.find_element(By.CSS_SELECTOR, ".card_photo div a img").get_attribute('src')
        event_instance = container.find_element(By.CSS_SELECTOR, ".card_content-title")
        event_link = event_instance.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        event_name = event_instance.find_element(By.CSS_SELECTOR, "a span").text
        event_body = container.find_elements(By.CSS_SELECTOR, ".card_content div")
        event_type = container.find_element(By.CSS_SELECTOR, ".card_footer a").text
        for event_data in event_body:
            try:
                event_date = event_data.text
            except NoSuchElementException as E:
                event_date = ''
            try:
                event_location = event_data.find_element(By.CSS_SELECTOR, "a span").text
            except NoSuchElementException as E:
                event_location = ''
        events_data[event_name] = {
            'image_link': event_img,
            'event_name': event_name,
            'event_link': event_link,
            'event_type': event_type,
            'event_date': event_date,
            'event_location': event_location
        }
        print(events_data)
    return driver_instance


def get_events_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome("path/to/chromedriver.exe",
                              options=options)
    try:
        driver.get("https://www.yelp.com/events")
        time.sleep(2)
        more_events = driver.find_element(By.CSS_SELECTOR, ".va-grid div a")
        time.sleep(2)
        action_chains = ActionChains(driver)
        action_chains.key_down(Keys.CONTROL).click(more_events).key_up(Keys.CONTROL).perform()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        extract_events(driver)
        while len(driver.find_elements(By.CSS_SELECTOR, ".arrange_unit .next")) > 0:
            next_element = driver.find_element(By.CSS_SELECTOR, ".arrange_unit .next")
            action_chains = ActionChains(driver)
            action_chains.key_down(Keys.CONTROL).click(next_element).key_up(Keys.CONTROL).perform()
            driver.switch_to.window(driver.window_handles[-1])
            extract_events(driver)
        driver.quit()
    except Exception as E:
        print(E)
    return events_data
