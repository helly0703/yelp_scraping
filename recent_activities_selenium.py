import time
from selenium import webdriver
from selenium.webdriver.common.by import By

all_activities = {}


def list_activities(driver_instance):
    elements = driver_instance.find_elements(By.CLASS_NAME, "container__09f24__YTiCU")
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


def get_recent_activities_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome("path/to/chromedriver.exe",
                              options=options)
    try:

        driver.get("https://www.yelp.com/")
        time.sleep(3)
        list_activities(driver)
        while len(all_activities) < 50:
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the "Show Next" button to be clickable
            show_next_button = driver.find_element(By.XPATH, "//*[text()='Show more activity']")

            # Click the "Show Next" button
            show_next_button.click()
            list_activities(driver)
        driver.quit()
    except Exception as E:
        print(E)
    return all_activities
