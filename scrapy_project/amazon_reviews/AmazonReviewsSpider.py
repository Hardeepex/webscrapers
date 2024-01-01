import scrapy
from selectolax.parser import HTMLParser
from selenium import webdriver


class AmazonReviewsSpider(scrapy.Spider):
    name = 'amazon_reviews'
    start_urls = ['https://www.amazon.com/product-reviews/B08N5WRWNW']

    def parse(self, response):
        driver = webdriver.Firefox()
        driver.get(response.url)
        html = driver.page_source
        driver.close()

        for node in HTMLParser(html).css('div.review'):
            yield {
                'title': node.css_first('a.review-title span').text(),
                'rating': node.css_first('i.review-rating span').text(),
                'body': node.css_first('span.review-text').text(),
            }
