"""This module contains the ``SeleniumMiddleware`` scrapy middleware"""


from fake_useragent import UserAgent
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions
from undetected_chromedriver import Chrome
from undetected_chromedriver import ChromeOptions
from .http import SeleniumRequest
from .utils import SCRIPT


class SeleniumMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(self, driver_arguments):
        """Initialize the selenium webdriver

        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_executable_path: str
            The path of the executable binary of the driver
        driver_arguments: list
            A list of arguments to initialize the driver
        browser_executable_path: str
            The path of the executable binary of the browser
        """

        driver_options = ChromeOptions()
        driver_options.add_argument('start-maximized')
        prefs = {
            'profile.managed_default_content_settings.images': 2,  # Disable images
        }
        driver_options.page_load_strategy = 'eager'
        driver_options.add_experimental_option('prefs', prefs)
        # driver_options.add_experimental_option(
        #     'excludeSwitches', ['disable-popup-blocking']
        # )
        # driver_options.add_experimental_option(
        #     'excludeSwitches', ['enable-automation']
        # )
        # driver_options.add_experimental_option('useAutomationExtension', False)
        for argument in driver_arguments:
            driver_options.add_argument(argument)
        # ua = UserAgent().random
        # driver_options.add_argument(f'user-agent={ua}')
        self.driver = Chrome(options=driver_options)
        # ua = get_random_chrome_user_agent()
        # stealth(
        #     driver=self.driver,
        #     user_agent=ua,
        #     languages=['ru-RU', 'ru'],
        #     vendor='Google Inc.',
        #     platform='Win32',
        #     webgl_vendor='Intel Inc.',
        #     renderer='Intel Iris OpenGL Engine',
        #     fix_hairline=True,
        #     run_on_insecure_origins=False,
        # )
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {
                'source': """
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """
            },
        )

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        driver_arguments = crawler.settings.get(
            'SELENIUM_DRIVER_ARGUMENTS', []
        )

        middleware = cls(
            driver_arguments=driver_arguments,
        )

        crawler.signals.connect(
            middleware.spider_closed, signals.spider_closed
        )

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        if not isinstance(request, SeleniumRequest):
            return None

        # Add cookies before loading the page
        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie(
                {'name': cookie_name, 'value': cookie_value}
            )

        self.driver.get(request.url)
        WebDriverWait(self.driver, 3)
        self.driver.execute_script(SCRIPT)
        try:
            if request.wait_until:
                WebDriverWait(self.driver, request.wait_time).until(
                    request.wait_until
                )
        except TimeoutException:
            spider.logger.error(f'Timeout waiting for {request.url}')
            return HtmlResponse(
                self.driver.current_url,
                body=str.encode(''),
                encoding='utf-8',
                request=request,
            )

        if request.script:
            self.driver.execute_script(request.script)

        if request.screenshot:
            request.meta['screenshot'] = self.driver.get_screenshot_as_png()

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request,
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""

        self.driver.quit()


def get_random_chrome_user_agent():
    user_agent = UserAgent(browsers='chrome', os='windows', platforms='pc')
    return user_agent.random
