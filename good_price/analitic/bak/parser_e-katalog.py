import requests
import csv
import time
from typing import List

from lxml import html
from fake_headers import Headers
from bs4 import BeautifulSoup

from exceptions import ParserFindTagException, IncomingDataIsMissingException
from utils import find_tag


HEADERS = Headers(
        browser="chrome",
        os="win",
        headers=True
    ).generate()
URL = 'https://ek.ua/list/186/'
DOMAIN = 'https://ek.ua/'
ALL_DATA = dict()
QUEUE_URL = set()
PROXIES = {
        'https': 'http://inulgvqm:drzeljplcnbh@64.64.118.149:6732'
    }


def add_to_csv_from_file(product_dict):

    with open('data.csv', 'a') as csvfile:
        fieldnames = ["Name", "Price", "Url", "Title"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,
                                quoting=csv.QUOTE_ALL)
        writer.writerow(product_dict)


def get_all_pages_of_category(category_link: str) -> List[str]:
    '''Получить ссылки на все страницы категории'''

    response = requests.get(category_link, headers=HEADERS, proxies=PROXIES)
    soup = BeautifulSoup(response.text, features='lxml')

    page_nums = find_tag(soup, 'div', attrs={'class': 'ib page-num'})

    pages_count = page_nums.find_all('a', class_='ib')[-1].get_text()

    if not pages_count:
        raise ParserFindTagException('Не найдены теги "a" с классом "ib"')

    category_id = category_link.split('/')[4]
    return [f'https://ek.ua/list/{category_id}/{page_num}/'
            for page_num in range(int(pages_count))]


def get_product_links(category_links: List[str]) -> List[str]:
    '''Пролучить все ссылки на товары со страниц'''
    print(category_links)

    if category_links:
        products_links = []
        for category_link in category_links:
            response = requests.get(
                category_link, headers=HEADERS, proxies=PROXIES
            )
            soup = BeautifulSoup(response.text, features='lxml')

            products_list = soup.find('form', id='list_form1')
            if not products_list:
                # Зачастую это баг самого e-katalog, но можно
                # это включить и в логирование.
                print(f'На странице {category_link} нет товаров')
                continue

            products = products_list.find_all(
                'a', class_='model-short-title'
            )
            for product in products:
                products_links.append(product['href'])

            time.sleep(2)

        return products_links
    else:
        raise IncomingDataIsMissingException('Нет ссылок на страницы товаров!')

    # for link in products_links:
    #     link['href']

    # product = dict()
    # request = requests.get(product_link, headers=HEADERS)
    # tree = html.fromstring(request.content)
    # product_name = tree.xpath("//h1/text()")
    # product_price = tree.xpath(
    #     "//div[@class='desc-short-prices'][1]//"
    #     "div[@class='desc-big-price ib']//span[1]/text()"
    # )
    # product['Url'] = product_link
    # product['Title'] = tree.findtext('.//title')
    # for name in product_name:
    #     product['Name'] = name
    # for price in product_price:
    #     product['Price'] = price
    # time.sleep(3)
    # print('Ñáîð äàííûõ ñ URL', product_link)

    # return product


def get_links(page_url):

    pagination_pages = set()
    request = requests.get(page_url, headers=HEADERS)
    tree = html.fromstring(request.content)
    pages_count = tree.xpath('//div[@class="ib page-num"]//a[last()]/text()')
    print('Статус код ответа:', request.status_code)
    print('Количество страниц с товаром:', pages_count)

    for url in range(int(pages_count[0])):
        full_url = f"https://ek.ua/list/186/{url}/"
        pagination_pages.add(full_url)

    while len(pagination_pages) != 0:
        current_url = pagination_pages.pop()
        print('Текущий обрабатываемый URL:', current_url)
        request = requests.get(current_url, headers=HEADERS)
        tree = html.fromstring(request.content)
        links = tree.xpath("//a[@class='model-short-title no-u']/@href")
        for link in links:
            QUEUE_URL.add(DOMAIN+link)
        time.sleep(3)


def main():
    # with open('data.csv', 'a') as csvfile:
    #     fieldnames = ["Name", "Price", "Url", "Title"]
    #     writer = csv.DictWriter(
    #         csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL
    #     )
    #     writer.writeheader()

    # get_links(URL)
    QUEUE_URL.add('https://ek.ua/list/186/0/')

    while len(QUEUE_URL) != 0:
        current_url = QUEUE_URL.pop()
        # add_to_csv_from_file(get_data(current_url))
        get_product_links(current_url)


if __name__ == "__main__":
    # main()
    print(
        get_product_links(
            get_all_pages_of_category('https://ek.ua/list/192/')
        )
    )
    # print(get_all_pages_of_category('https://ek.ua/list/192/'))
