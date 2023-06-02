import re
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_email_data():
    email_list = []
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome("path/to/chromedriver.exe",
                              options=options)
    driver.get("https://www.yelp.com/")
    links = driver.find_elements(By.TAG_NAME, 'a')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    for link in links:
        href = link.get_attribute('href')
        if href:
            email_matches = email_pattern.findall(href)
            if email_matches:
                for email in email_matches:
                    email_list.append(email)
    driver.quit()
    return email_list if email_list != [] else "No emails found"
