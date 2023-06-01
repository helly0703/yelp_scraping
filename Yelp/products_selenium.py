import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
try:
    driver.get("https://www.yelp.com/")
    time.sleep(3)
    elements = driver.find_elements(By.CLASS_NAME, "header-link_anchor__09f24__eCD4u")
    time.sleep(2)
    products = {}
    for element in elements:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(2)
        product = element.text
        hovered_element = driver.find_element(By.TAG_NAME,"menu")
        time.sleep(2)
        products_list = []
        categories = hovered_element.find_elements(By.TAG_NAME,'span')
        time.sleep(1)
        for i in categories:
            category = i.text
            if category != '':
                products_list.append(category)
        products[product] = products_list
except Exception as E:
    print(E)