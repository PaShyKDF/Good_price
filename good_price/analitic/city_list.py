from typing import List

from requests_html import HTMLSession
from bs4 import BeautifulSoup

from .constants import CITIES_LINK


def get_cities() -> List[dict]:
    '''Функция возвращает список словарей городов
    с населением более 100_000 человек\n
    {'name': 'Новошахтинск', 'country': 'Россия'}'''

    session = HTMLSession()
    response = session.get(CITIES_LINK)
    soup = BeautifulSoup(response.html.html, 'lxml')
    city_table = soup.find('tbody')
    city_cards = city_table.find_all('tr')[2:]
    # city_list = [None] * len(city_cards)
    city_list = []
    # for num, city_card in enumerate(city_cards):
    for city_card in city_cards:
        city_list.append(
            {'name': city_card.find('a').text, 'country': 'Россия'}
        )
    return city_list


if __name__ == '__main__':
    print(get_cities())
