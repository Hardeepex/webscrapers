from urllib.parse import urljoin

import scrapy
from selectolax.parser import HTMLParser
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from yourproject.items import YourItem


class MySpider(scrapy.Spider):
    name = 'my_spider'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/c/camping-and-hiking/f/scd-deals']

    def __init__(self):
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
        )

    def parse(self, response):
        self.driver.get(response.url)
        selenium_response_text = self.driver.page_source
        html = HTMLParser(selenium_response_text)
        product_nodes = html.css('li.c-product-card')
        for node in product_nodes:
            product_url = urljoin(response.url, node.css_first("a").attributes["href"])
            yield scrapy.Request(product_url, self.parse_item_page)
        next_page_url = self.get_next_page_url(html)
        if next_page_url:
            yield scrapy.Request(next_page_url, self.parse)

    def parse_item_page(self, response):
        item = YourItem()
        # populate item fields here
        yield item

    def get_next_page_url(self, html):
        next_page_node = html.css_first('.pagination .next')
        if next_page_node:
            return urljoin('http://example.com', next_page_node.attributes['href'])
        return None

    def closed(self, reason):
        self.driver.quit()
