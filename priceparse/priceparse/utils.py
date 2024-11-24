import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SCRIPT = """
    var scrollInterval = 100; // adjust the scroll interval to your liking
    var scrollTo = 1800; // adjust the scroll position to your liking
    var currentScroll = 0;

    function scrollDown() {
        currentScroll += scrollInterval;
        window.scrollTo(0, currentScroll);
        if (currentScroll < scrollTo) {
            setTimeout(scrollDown, 50); // adjust the timeout to your liking
        }
    }

    scrollDown();
"""


def scroll_and_load(driver):
    last_height = driver.execute_script('return document.body.scrollHeight')

    while True:
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);'
        )
        time.sleep(2)  # Allow time for new content to load

        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break  # Exit if no new content loaded
        last_height = new_height


def click_button(driver, script):
    while True:
        try:
            # Wait for the iframe to load and switch to it if necessary\
            # Wait for the button to be present and clickable
            driver.execute_script(script)
            WebDriverWait(driver, 200).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        'button-ui.button-ui_grey.button-ui_lg.product-characteristics__expand',
                    )
                )
            )
            button = driver.find_element_by_css_selector(
                'button-ui.button-ui_grey.button-ui_lg.product-characteristics__expand'
            )
            # Try clicking the button
            button.click()
            print('Button clicked successfully.')
            return

        except TimeoutException:
            print('Timeout: Button not found or not clickable.')
            driver.refresh()
            print('Refreshing...')

        except NoSuchElementException:
            driver.refresh()
            print('Error: Button does not exist.')
            print('Refreshing...')

        except Exception as e:
            if 'element click intercepted' in str(e):
                print('An unexpected error occurred: Element click intercepted.')
                input_field = driver.find_element_by_css_selector(
                    'input.presearch__input'
                )
                input_field.click()
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth'})", input_field
                )
            else:
                print(f'An unexpected error occurred: {e}')
            driver.refresh()
            print('Refreshing...')

