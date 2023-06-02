import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from undetected_chromedriver import Chrome, ChromeOptions

articles_data = {}


def extract_articles(driver_instance):
    time.sleep(2)
    containers = driver_instance.find_elements(By.CSS_SELECTOR, ".c-card--has-image")
    for container in containers:
        article_link = container.find_element(By.CSS_SELECTOR, ".c-card__media .c-card__link").get_attribute('href')
        article_image = container.find_element(By.CSS_SELECTOR, ".c-card__media .c-card__image img").get_attribute(
            'src')
        article_content = container.find_element(By.CSS_SELECTOR, ".c-card__content")
        article_tag = article_content.find_element(By.CSS_SELECTOR, ".t-tag").text
        article_title = article_content.find_element(By.CSS_SELECTOR, ".c-card__title").text
        article_date = article_content.find_element(By.CSS_SELECTOR, ".c-card__date").text
        articles_data[article_title] = {
            'article_title': article_title,
            'article_image': article_image,
            'article_link': article_link,
            'article_date': article_date,
            'article_tag': article_tag
        }
    return driver_instance


def get_articles_data():
    options = ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode

    driver = Chrome(executable_path='/path/to/chromedriver',options=options)
    try:
        driver.get("https://blog.yelp.com/")
        time.sleep(4)
        more_articles = driver.find_elements(By.CLASS_NAME, "b-content-loop--layout_row")
        for article in more_articles:
            time.sleep(2)
            link = article.find_element(By.CLASS_NAME, 'c-content-block__cta-link')
            action_chains = ActionChains(driver)
            action_chains.key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)
            extract_articles(driver)
            driver.switch_to.window(driver.window_handles[0])
        driver.quit()
    except Exception as E:
        print(E)
    return articles_data
