import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://www.yelp.com/")
links = driver.find_elements(By.TAG_NAME, 'a')
email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

for link in links:
    href = link.get_attribute('href')
    if href:
        email_matches = email_pattern.findall(href)
        if email_matches:
            for email in email_matches:
                print(email)
driver.quit()
