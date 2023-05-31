import time

import scrapy
from playwright.async_api import async_playwright
from scrapy.http import HtmlResponse
from lxml import html

class YelpscrapSpider(scrapy.Spider):
    name = "YelpScrap"
    allowed_domains = ["www.yelp.com"]
    start_urls = ["https://www.yelp.com/"]

    async def parse(self, response):
        products = response.css('.header-nav_unit div a span::text').getall()
        print(products)
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()
            await page.goto(response.url)
            popup_data_list =[]
            elements = await page.query_selector_all('.header-link_anchor__09f24__eCD4u')
            for element in elements:
                time.sleep(2)
                await element.hover()

                # Extract data from the popup using Playwright
                popup = await page.query_selector('menu')
                popup_data = await popup.inner_html()
                popup_data_list.append(popup_data)
            await browser.close()
            for popup_data in popup_data_list:
                html_document = html.fromstring(popup_data)
                data = html_document.cssselect('span')
                for span in data:
                    span_text = span.text_content().strip()
                    print("Span Text:", span_text)

