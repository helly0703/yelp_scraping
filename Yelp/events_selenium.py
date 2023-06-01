import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

events_data = {}


def extract_events(driver_instance):
    containers = driver.find_elements(By.CSS_SELECTOR, ".card")
    time.sleep(2)
    for container in containers:
        event_img = container.find_element(By.CSS_SELECTOR,".card_photo div a img").get_attribute('src')
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
            'image_link':event_img,
            'name': event_name,
            'link': event_link,
            'type': event_type,
            'date': event_date,
            'location': event_location
        }
    return driver_instance


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
try:
    driver.get("https://www.yelp.com/events")
    time.sleep(2)
    more_events = driver.find_element(By.CSS_SELECTOR, ".va-grid div a")
    time.sleep(2)
    action_chains = ActionChains(driver)
    action_chains.key_down(Keys.CONTROL).click(more_events).key_up(Keys.CONTROL).perform()
    driver.switch_to.window(driver.window_handles[-1])
    extract_events(driver)
    while True:
        time.sleep(2)
        if len(driver.find_elements(By.CSS_SELECTOR, ".arrange_unit .next")) <= 0:
            break
        next_element = driver.find_element(By.CSS_SELECTOR, ".arrange_unit .next")
        action_chains = ActionChains(driver)
        action_chains.key_down(Keys.CONTROL).click(next_element).key_up(Keys.CONTROL).perform()
        driver.switch_to.window(driver.window_handles[-1])
        extract_events(driver)
    driver.quit()
except Exception as E:
    print(E)