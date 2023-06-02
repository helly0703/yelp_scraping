import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_products_data():
    products = {}
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome("path/to/chromedriver.exe",
                              options=options)
    try:
        driver.get("https://www.yelp.com/")
        time.sleep(2)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-link_anchor__09f24__eCD4u")))
        elements = driver.find_elements(By.CLASS_NAME, "header-link_anchor__09f24__eCD4u")
        for element in elements:
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            product = element.text
            hovered_element = driver.find_element(By.TAG_NAME, "menu")
            products_list = []
            categories = hovered_element.find_elements(By.TAG_NAME, 'span')
            for i in categories:
                category = i.text
                if category != '':
                    products_list.append(category)
            products[product] = products_list
    except Exception as E:
        print(E)
    return products
