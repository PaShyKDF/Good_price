import time
from typing import Dict, Union

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from good_price.analitic.utils import clock_to_float


def get_dns_products_name_price_link(city):
    '''
    Функция возвращает название, цену и ссылку на товар
    с страницы со списком товаров
    '''
    options = Options()
    options.page_load_strategy = 'none'

    driver = uc.Chrome(
        options=options, headless=False, use_subprocess=False
    )
    URL = 'https://www.dns-shop.ru/catalog/17a899cd16404e77/processory/'

    driver.get(URL)
    time.sleep(7)

    change_city = driver.find_element(By.CLASS_NAME, 'city-select__label_t33')
    change_city.click()
    time.sleep(3)

    city_input = driver.find_element(
        By.CLASS_NAME,
        '_base-ui-input-search__input_1jsxq_67'
    )
    city_input.clear()
    city_input.send_keys(city)
    time.sleep(3)

    select_sity = driver.find_element(
        By.CLASS_NAME,
        '_modal-row_x2e9p_7'
    )
    select_sity.click()
    time.sleep(3)

    while True:

        try:
            next_page_link = driver.find_element(
                By.CLASS_NAME,
                'pagination-widget__show-more-btn'
            )

            if next_page_link:
                next_page_link.click()
                time.sleep(5)
        except NoSuchElementException:
            print("No more pages available")
            break

    product_cards = driver.find_elements(
        By.CSS_SELECTOR,
        'div.catalog-product.ui-button-widget'
    )

    products_links = []
    for product in product_cards:
        name = ' '.join(product.find_element(
            By.TAG_NAME,
            'span'
        ).text.split('[')[0].strip().split(' ')[1:-1])
        price = product.find_element(
            By.CLASS_NAME,
            'product-buy__price'
        ).text
        link = product.find_element(
            By.CLASS_NAME,
            'catalog-product__name.ui-link.ui-link_black'
        ).get_attribute('href')
        price = int(price.replace(' ', '').rstrip('₽'))
        products_links.append((name, price, link))

    driver.close()
    driver.quit()
    return products_links


# def get_characteristics(div: WebElement) -> List[str]:
#     '''Получить характеристики из div с классом:\n
#     "product-characteristics__group product-characteristics__ovh"'''
#     try:
#         specifications = div.find_elements(
#             By.CLASS_NAME,
#             'product-characteristics__spec.product-characteristics__ovh'
#         )
#         product_specifications = []
#         for specification in specifications:
#             value = specification.find_element(
#                 By.CLASS_NAME,
#                 'product-characteristics__spec-value'
#             ).text.strip()
#             product_specifications.append(
#                 int(value) if value.isdigit() else value
#             )
#         return product_specifications
#     except Exception as ex:
#         print(f'Get characteristics Exeption: {ex}')


# def get_dns_processory_info(url: str) -> Dict[str, Union[str, int]]:
#     '''Получить все характеристики процессора'''
#     processory_info = {}

#     options = Options()
#     options.page_load_strategy = 'none'

#     driver = uc.Chrome(headless=False, use_subprocess=True)

#     driver.get(url)
#     time.sleep(3)

#     product_characteristics_expand = driver.find_element(
#         By.CLASS_NAME, 'product-characteristics__expand'
#     )
#     product_characteristics_expand.click()
#     time.sleep(3)

#     # product_characteristics = driver.find_element(
#     #     By.CLASS_NAME, 'product-card-description'
#     # )

#     '''Получение названия процессора'''
#     product_card_description = driver.find_element(
#         By.XPATH,
#         '//div[@class="product-characteristics__group"]/following-sibling::div'
#     )
#     name = product_card_description.find_element(
#         By.CLASS_NAME,
#         'product-characteristics__spec-value'
#     ).text
#     processory_info['name'] = name

#     '''Получение комплектации'''
#     product_card_title = driver.find_element(
#         By.CLASS_NAME, 'product-card-top__title'
#     ).text
#     equipment = product_card_title.split(' ')[-1]
#     processory_info['equipment'] = equipment

#     '''Получение сокета'''
#     general_parameters = product_card_description.find_element(
#         By.XPATH,
#         './div[@class="product-characteristics__spec"]/following-sibling::div'
#     )
#     try:
#         socket = general_parameters.find_element(
#             By.CLASS_NAME,
#             'ui-link.ui-link_blue.ui-link_pseudolink'
#         ).text.strip()
#     except NoSuchElementException:
#         socket = general_parameters.find_element(
#             By.CLASS_NAME,
#             'product-characteristics__spec-value'
#         ).text.strip()
#     processory_info['socket'] = socket

#     '''Получение ядер и кэша'''
#     core_and_architecture = driver.find_element(
#         By.CLASS_NAME,
#         'product-characteristics__group.product-characteristics__ovh'
#     )

#     characteristics = get_characteristics(core_and_architecture)

#     processory_info['cores_amount'] = characteristics[0]
#     if characteristics[0] == characteristics[1]:
#         processory_info['productive_cores_amount'] = 0
#     else:
#         processory_info['productive_cores_amount'] = characteristics[1]
#     processory_info['energy_efficient_cores_amount'] = characteristics[2]
#     processory_info['threads_amount'] = characteristics[3]
#     processory_info['second_level_cache'] = characteristics[4]
#     processory_info['third_level_cache'] = characteristics[5]
#     processory_info['tech_process'] = characteristics[6]

#     '''Получение частот'''
#     frequencies = driver.find_element(
#         By.XPATH,
#         '//div[@class="product-characteristics__group '
#         'product-characteristics__ovh"]/following-sibling::div'
#     )

#     characteristics = get_characteristics(frequencies)

#     processory_info['clock_frequency'] = clock_to_float(
#         characteristics[0]
#     )
#     processory_info['turboboost_frequency'] = clock_to_float(
#         characteristics[1]
#     )
#     free_multiplier = ('да' if characteristics[4] == 'есть' else 'нет')
#     processory_info['free_multiplier'] = free_multiplier

#     '''Получение типа ОЗУ'''
#     RAM_characteristics = driver.find_element(
#         By.XPATH,
#         '//div[@class="product-characteristics__group product-'
#         'characteristics__ovh"]/following-sibling::div/following-sibling::div'
#     )

#     characteristics = get_characteristics(RAM_characteristics)

#     processory_info['RAM_support'] = characteristics[0]

#     '''Получение тепловыделения'''
#     heat_dissipation = driver.find_element(
#         By.XPATH,
#         '//div[@class="product-characteristics__group product-'
#         'characteristics__ovh"]/following-sibling::div/following-sibling::div/'
#         'following-sibling::div'
#     )

#     characteristics = get_characteristics(heat_dissipation)

#     processory_info['tdp'] = characteristics[0]

#     '''Получение наличия встроенного графического ядра'''
#     graphics_core = driver.find_element(
#         By.XPATH,
#         '//div[@class="product-characteristics__group product-'
#         'characteristics__ovh"]/following-sibling::div/following-sibling::div/'
#         'following-sibling::div/following-sibling::div'
#     )

#     characteristics = get_characteristics(graphics_core)

#     graphics_core = ('да' if characteristics[0] == 'есть' else 'нет')
#     processory_info['graphics_core'] = graphics_core

#     driver.close()
#     driver.quit()
#     return processory_info


def get_dns_processory_info(url: str) -> Dict[str, Union[str, int]]:
    '''Получить все характеристики процессора'''
    processory_info = {}

    options = Options()
    options.page_load_strategy = 'none'

    driver = uc.Chrome(options=options, headless=False, use_subprocess=True)

    driver.get(url)
    time.sleep(5)
    driver.execute_script('window.scrollTo(0, 2000)')
    time.sleep(1)

    product_characteristics_expand = driver.find_element(
        By.CLASS_NAME,
        'button-ui.button-ui_grey.button-ui_lg.product-characteristics__expand'
    )
    product_characteristics_expand.click()
    time.sleep(3)

    '''Получение комплектации'''
    product_card_title = driver.find_element(
        By.CLASS_NAME, 'product-card-top__title'
    ).text
    equipment = product_card_title.split(' ')[-1]
    processory_info['equipment'] = equipment

    '''Получение основных характеристик из таблицы'''
    characteristics_table = driver.find_element(
        By.CLASS_NAME, 'product-characteristics-content'
    )
    characteristics = characteristics_table.find_elements(
        By.CSS_SELECTOR, 'li.product-characteristics__spec'
    )

    processory_data = {}
    for characteristic in characteristics:
        title = characteristic.find_element(By.CSS_SELECTOR, 'span').text
        value = characteristic.find_element(
            By.CLASS_NAME, 'product-characteristics__spec-value'
        ).text
        processory_data[title] = value

    '''Распределение характеристик'''
    processory_info['name'] = processory_data.get('Модель')
    processory_info['socket'] = processory_data.get('Сокет')

    cores_amount = processory_data.get('Общее количество ядер')
    processory_info['cores_amount'] = cores_amount

    productive_cores_amount = processory_data.get(
        'Количество производительных ядер'
    )
    if cores_amount == productive_cores_amount:
        processory_info['productive_cores_amount'] = 0
    else:
        processory_info['productive_cores_amount'] = productive_cores_amount

    processory_info['energy_efficient_cores_amount'] = processory_data.get(
        'Количество энергоэффективных ядер'
    )
    processory_info['threads_amount'] = processory_data.get(
        'Максимальное число потоков'
    )
    processory_info['second_level_cache'] = processory_data.get(
        'Объем кэша L2'
    )
    processory_info['third_level_cache'] = processory_data.get(
        'Объем кэша L3'
    )
    processory_info['tech_process'] = processory_data.get('Техпроцесс')
    processory_info['clock_frequency'] = clock_to_float(
        processory_data.get('Базовая частота процессора')
    )
    processory_info['turboboost_frequency'] = clock_to_float(
        processory_data.get('Максимальная частота в турбо режиме')
    )
    free_multiplier = processory_data.get('Свободный множитель')
    if free_multiplier is not None:
        processory_info['free_multiplier'] = (
            'да' if free_multiplier == 'есть' else 'нет'
        )
    processory_info['RAM_support'] = processory_data.get('Тип памяти')
    processory_info['tdp'] = processory_data.get('Тепловыделение (TDP)')
    processory_info['graphics_core'] = (
        'да'
        if processory_data.get('Интегрированное графическое ядро') == 'есть'
        else 'нет'
    )

    driver.close()
    driver.quit()
    return processory_info


if __name__ == '__main__':
    print(get_dns_processory_info('https://www.dns-shop.ru/product/057676b27'
                                  'db03330/processor-amd-athlon-x4-950-oem/'))
    # products_links = get_dns_products_name_price_link('Воронеж')
    # print(products_links)
    # for link in products_links:
    #     get_processory_info(link)
