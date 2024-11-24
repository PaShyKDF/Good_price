
import scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..http import SeleniumRequest
from ..utils import click_button

SCRIPT = """
    var scrollInterval = 100; // adjust the scroll interval to your liking
    var scrollTo = 2000; // adjust the scroll position to your liking
    var currentScroll = 0;

    function scrollDown() {
        currentScroll += scrollInterval;
        window.scrollTo(0, currentScroll);
        if (currentScroll < scrollTo) {
            setTimeout(scrollDown, 50); // adjust the timeout to your liking
        }
    }

    scrollDown();
"""  # Script to scroll down the page smoothly
# Script to scroll down the page


class DnsSpider(scrapy.Spider):
    name = 'dns'
    start_urls = [
        'https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse_dns,
                wait_time=200,
                wait_until=EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, '.product-buy__price')
                ),
            )

    def parse_dns(self, response):
        driver = response.meta['driver']
        product_cards = response.css('div.catalog-product.ui-button-widget')

        for product in product_cards:
            name = product.css('a span::text').get(default='').strip()
            price = (
                product.css('.product-buy__price::text')
                .get(default='')
                .strip()
            )
            link = response.urljoin(
                product.css(
                    '.catalog-product__name.ui-link.ui-link_black::attr(href)'
                ).get(default='')
            )
            yield SeleniumRequest(
                url=link,
                callback=self.parse_processor_info,
                script=SCRIPT,
                meta={'driver': driver, 'name': name, 'price': price},
            )

        next_page = response.css(
            '.pagination-widget__page-link_next::attr(href)'
        ).get()
        if next_page:
            yield SeleniumRequest(
                url=response.urljoin(next_page),
                callback=self.parse_dns,
                wait_time=200,
                wait_until=EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, '.product-buy__price')
                ),
                script=SCRIPT,
                meta={'driver': driver},
            )

    def parse_processor_info(self, response):
        driver = response.meta['driver']
        processor_info = {
            'name': response.meta['name'],
            'price': response.meta['price'],
        }

        click_button(driver, SCRIPT)

        print('Clicked button successfully')

        # Extract characteristics
        while True:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '.product-characteristics-content li.product-characteristics__spec',
                    )
                )
            )
            characteristics = driver.find_elements(
                By.CSS_SELECTOR,
                '.product-characteristics-content li.product-characteristics__spec',
            )
            if characteristics:
                for characteristic in characteristics:
                    title = characteristic.find_element(
                        By.CSS_SELECTOR, 'span'
                    ).text.strip()
                    value = characteristic.find_element(
                        By.CSS_SELECTOR, '.product-characteristics__spec-value'
                    ).text.strip()
                    processor_info[title] = value
                break
            print('Characteristics not found, retrying...')
            driver.refresh()
            click_button(driver, SCRIPT)

        yield processor_info

    def clock_to_float(self, clock_frequency):
        if clock_frequency:
            clock_frequency = clock_frequency.strip()
            clock = float(clock_frequency.split(' ')[0])
            return (
                clock / 1000 if clock > 100 else clock
            )  # Convert MHz to GHz if necessary
        return None

