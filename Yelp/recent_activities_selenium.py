import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

all_activities = {}


def list_activities(driver_instance):
    elements = driver_instance.find_elements(By.CLASS_NAME, "container__09f24__YTiCU")
    time.sleep(2)
    for element_val in elements:
        activity_by = element_val.find_element(By.CSS_SELECTOR, ".user-passport-info span a")
        activity = element_val.find_element(By.CLASS_NAME, "link__09f24__nEC8H")
        activity_name = activity.text
        activity_link = activity.get_attribute('href')

        if activity_name != '' and activity_name not in all_activities:
            activity_details = {
                'name': activity_name,
                'link': activity_link,
                'author': activity_by.text
            }
            all_activities[activity_name] = activity_details
    return driver_instance


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
try:

    driver.get("https://www.yelp.com/")
    wait = WebDriverWait(driver, 10)
    time.sleep(3)
    list_activities(driver)
    while True:
        time.sleep(1)
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the "Show Next" button to be clickable
        show_next_button = driver.find_element(By.XPATH, "//*[text()='Show more activity']")

        # Click the "Show Next" button
        show_next_button.click()
        time.sleep(3)
        # Extract the data from the current page
        list_activities(driver)

        # Check if there is no "Show Next" button, indicating the end of the data
        if len(all_activities) >= 50:
            break
        # if not show_next_button.is_displayed():
        #     break
except Exception as E:
    print(E)
