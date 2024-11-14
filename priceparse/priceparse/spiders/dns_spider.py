# myproject/spiders/dns_spider.py
import time

import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from ..http import SeleniumRequest


class DnsSpider(scrapy.Spider):
    name = 'dns'
    start_urls = [
        'https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse_dns,
                wait_time=2,
                wait_until=EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div.catalog-product.ui-button-widget')
                ),
                script='window.scrollTo(0, document.body.scrollHeight-100);',
            )

    def parse_dns(self, response):
        product_cards = response.css('div.catalog-product.ui-button-widget')
        for product in product_cards:
            name = product.css('a').css('span::text').get('').strip()
            price = product.css('.product-buy__price::text').get('').strip()
            link = product.css(
                '.catalog-product__name.ui-link.ui-link_black::attr(href)'
            ).get('')
            yield {'name': name, 'price': price, 'link': link}

        # Handle pagination
        next_page = response.css(
            '.pagination-widget__page-link_next::attr(href)'
        ).get()
        if next_page:
            yield SeleniumRequest(
                url='https://www.dns-shop.ru' + next_page,
                callback=self.parse_dns,
                wait_time=2,
                wait_until=EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, 'div.catalog-product.ui-button-widget')
                ),
                script='window.scrollTo(0, document.body.scrollHeight - 100);',
            )
