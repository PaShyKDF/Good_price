import re
import time
from typing import List

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from requests_html import HTMLSession
from bs4 import BeautifulSoup


# Имеет смысл парсить, т.к. в некоторые города не доставляют
def city_links():
    '''Функция возвращает список специфических названий
    городов, которые использует сайт Citilink'''

    driver = uc.Chrome(headless=False, use_subprocess=False)
    url = 'https://www.citilink.ru/catalog/processory/'

    driver.get(url)
    time.sleep(1)

    change_city = driver.find_element(
        By.CLASS_NAME,
        'e1x3msk40.css-wsr9k9.etyxved0'
    )
    change_city.click()
    time.sleep(3)

    cities = driver.find_elements(By.CLASS_NAME, 'css-741atx.e1g2mros0')
    for city_by_alphabet in cities:
        city_list = city_by_alphabet.find_elements(
            By.CLASS_NAME,
            'et1rfzz0.css-10tcptu.evy6na20'
        )
        for city in city_list:
            city_link = city.find_element(
                By.CLASS_NAME,
                'css-vrsjnq.e1mnvjgw0'
            ).get_attribute('href')
            print(city_link)
    driver.quit()


def get_category_pages(url: str) -> List[str]:
    '''По ссылке на категорию товара возвращает список url со страницами'''

    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=7, keep_page=True)
    soup = BeautifulSoup(response.html.html, 'lxml')

    paginate_bar = soup.select_one('div.app-catalog-ww4zz0.e1ywnng50')
    paginate_buttons = paginate_bar.select('a.app-catalog-peotpw.e1mnvjgw0')

    session.close()

    pages_count = int(paginate_buttons[-2].text)

    pages_list = []
    for enum in range(1, pages_count+1):
        pages_list.append(url + f'?p={enum}')
    return pages_list


def product_parser(urls: List[str]):
    '''Функция возвращает название и цену с страницы со списком товаров'''

    session = HTMLSession()
    count = 0
    for url in urls:
        response = session.get(url)
        response.html.render(sleep=7, keep_page=True)
        soup = BeautifulSoup(response.html.html, 'lxml')
        product_cards = soup.select(
            'div.e1ex4k9s0.app-catalog-1bogmvw.e1loosed0'
        )
        for product_card in product_cards:
            try:
                name = re.split(
                    r'\b(?:,  OEM|,  BOX)\b',
                    product_card.find(
                        'a', {'data-meta-name': 'Snippet__title'}
                        ).text)[0]
                price = product_card.select_one(
                    'span.e1j9birj0.e106ikdt0.app-catalog-56qww8.e1gjr6xo0'
                ).text
                link = product_card.select_one(
                    'a.app-catalog-9gnskf.e1259i3g0'
                ).get('href')
                print(name + ' - ' + price + ' ' + link)
                count += 1
                print()
            except AttributeError:
                print('Этого товара нет в наличии.')
    session.close()


if __name__ == '__main__':
    print(product_parser(
        [
            'https://www.citilink.ru/catalog/processory/?pf=available.all%2Cdi'
            'scount.any%2Crating.any&f=discount.any%2Crating.any%2Cavailable.'
            'instore'
        ]
    ))
