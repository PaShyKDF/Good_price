import time
import random
from typing import Dict, Union
import zipfile

from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from good_price.analitic.utils import (
    clock_to_float, cores_to_int, validate_graphics_core
)
from good_price.analitic.constants import PROXIES, USER_AGENTS


PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS = random.choice(
    PROXIES
).split(':')

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    chrome_options = webdriver.ChromeOptions()

    if use_proxy:
        # chrome_options.add_argument('--proxy-server=your_proxy:proxy_port')

        plugin_file = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('manifest.json', manifest_json)
            zp.writestr('background.js', background_js)

        chrome_options.add_extension(plugin_file)

    if user_agent:
        chrome_options.add_argument(
            f'--user-agent={random.choice(user_agent)}'
        )

    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_regard_products_name_price_link(city) -> tuple:
    '''
    Функция возвращает название, цену и ссылку на товар
    с страницы со списком товаров
    '''

    driver = uc.Chrome(headless=False, use_subprocess=False)
    url = 'https://www.regard.ru/catalog/1001/processory'

    driver.get(url)
    time.sleep(1)

    count_cards_on_page = driver.find_element(
        By.CSS_SELECTOR,
        'span.PaginationViewChanger_countSetter__count__65Dji'
    )
    count_cards_on_page.click()
    cards_100 = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'по 100')]"
    )
    cards_100.click()
    time.sleep(3)

    while True:

        try:
            next_page_link = driver.find_element(
                By.CSS_SELECTOR,
                'button.Button_button__GeQ2O.Button_medium__i68W9.'
                'Button_secondary__qJMHg.Pagination_loadMore__u1Wm_'
            )

            if next_page_link:
                next_page_link.click()
                time.sleep(5)
        except NoSuchElementException:
            print("No more pages available")
            break

    product_cards = driver.find_elements(
        By.CSS_SELECTOR,
        'div.Card_row__6_JG5'
    )
    products_links = []
    for product in product_cards:
        try:
            name = product.find_element(
                By.CLASS_NAME,
                'CardText_title__7bSbO.CardText_listing__6mqXC'
            ).text.rstrip(' (без кулера)')
            price = product.find_element(
                By.CLASS_NAME,
                'Price_price__m2aSe.notranslate'
            ).text
            link = product.find_element(
                By.CLASS_NAME,
                'CardText_link__C_fPZ.link_black'
            ).get_attribute('href')
            price = int(price.replace(' ', '').rstrip('₽'))
            products_links.append((name, price, link))
        except NoSuchElementException:
            print('У товара отсутствует цена')

    driver.close()
    driver.quit()

    return products_links


def get_regard_processory_info(
        url: str
) -> Dict[str, Union[str, int, float]]:
    '''
    Получить характеристики процессора с сайта regard
    '''

    # driver = webdriver.Chrome()
    driver = get_chromedriver(use_proxy=False, user_agent=USER_AGENTS)
    driver.get(url)
    time.sleep(3)

    processory_info = {}

    title = driver.find_element(
        By.CSS_SELECTOR, 'h1.Product_title__42hYI'
    ).text
    equipment = title.split(' ').pop()
    name = ' '.join(title.rstrip(' ' + equipment).split(' ')[1:])

    processory_info['name'] = name
    processory_info['equipment'] = equipment

    characteristics_table = driver.find_element(
        By.CLASS_NAME, 'ProductCharacteristics_masonry__Ut6Zp'
    )
    characteristics = characteristics_table.find_elements(
        By.CSS_SELECTOR, 'div.CharacteristicsItem_item__QnlK2'
    )

    processory_data = {}
    for characteristic in characteristics:
        title = characteristic.find_element(By.CSS_SELECTOR, 'span').text
        value = characteristic.find_element(
            By.CSS_SELECTOR, 'div[class^="CharacteristicsItem_value"]'
        ).text
        processory_data[title] = value

    processory_info['lineup'] = processory_data.get('Линейка')
    processory_info['socket'] = processory_data.get('Socket')
    processory_info['tech_process'] = processory_data.get(
        'Технологический процесс'
    )
    processory_info['clock_frequency'] = clock_to_float(
        processory_data.get('Тактовая частота')
    )
    processory_info['turboboost_frequency'] = clock_to_float(
        processory_data.get('Частота процессора в режиме Turbo')
    )
    processory_info['cores_amount'] = cores_to_int(
        processory_data.get('Количество ядер')
    )
    processory_info['productive_cores_amount'] = cores_to_int(
        processory_data.get('Высокопроизводительные ядра', 0)
    )
    processory_info['energy_efficient_cores_amount'] = cores_to_int(
        processory_data.get('Энергоэффективные ядра', 0)
    )
    processory_info['threads_amount'] = cores_to_int(
        processory_data.get('Количество потоков',
                            processory_info['cores_amount'])
    )
    processory_info['tdp'] = processory_data.get('Типичное тепловыделение')
    processory_info['second_level_cache'] = processory_data.get(
        'Объём кэша L2'
    )
    processory_info['third_level_cache'] = processory_data.get(
        'Объём кэша L3', '0 Мб'
    )
    processory_info['free_multiplier'] = processory_data.get(
        'Разблокированный множитель'
    )
    processory_info['graphics_core'] = validate_graphics_core(
        processory_data.get('Интегрированное графическое ядро')
    )

    driver.close()
    driver.quit()

    time.sleep(5)

    return processory_info


def main():
    # processories = get_regard_products_name_price_link('c')
    # print(processories)
    processories = [
        'https://www.regard.ru/product/260583/processor-amd-athlon-x4-950-oem'
    ]
    for processory in processories:
        print(get_regard_processory_info(processory))


if __name__ == '__main__':
    main()
