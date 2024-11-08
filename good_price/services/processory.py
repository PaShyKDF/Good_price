import asyncio
from typing import List

from good_price.crud.processory import processory_crud
from good_price.crud.parsed_site import parsed_site_crud
from good_price.crud.city import city_crud
from good_price.crud.processory_price import processory_price_crud
from good_price.core.db import AsyncSessionLocal
from good_price.services.validators import check_processory_exists
# from good_price.analitic.parser_regard import get_regard_processory_info
# from good_price.analitic.parser_dns_shop import get_dns_processory_info
from good_price.services.constants import (
    STORES_PRICE_NOT_DEPEND_ON_REGION, FUNCTIONS_DEPEND_ON_REGION,
    FUNCTIONS_NOT_DEPEND_ON_REGION  # , CHARACTERISTICS_FROM_DNS
)


async def get_cities():
    '''Получить все города из базы данных'''
    async with AsyncSessionLocal() as session:
        return await city_crud.get_cities_list(session)


async def create_update_processory_price(
        processory_id, store, price, cities_count, city
):
    '''Если цена уже есть, функция обновляет ее. Если цены нет, создает'''
    async with AsyncSessionLocal() as session:
        processory_price = await processory_price_crud.get_processory_price(
            processory_id, store, session
        )
        if processory_price is not None:
            if store in STORES_PRICE_NOT_DEPEND_ON_REGION:
                processory_prices = (
                    await processory_price_crud.get_processory_prices(
                        processory_id, store, session
                    )
                )
                price = {'price': price}
                await processory_price_crud.multiple_update(
                    processory_prices, price, session
                )
            else:
                price = {'price': price}
                await processory_price_crud.update(
                    processory_price, price, session
                )
        else:
            if store in STORES_PRICE_NOT_DEPEND_ON_REGION:
                for city_id in range(1, cities_count+1):
                    processory_price = {
                            'processory_id': processory_id,
                            'store': store,
                            'city_id': city_id,
                            'price': price
                    }
                    await processory_price_crud.create(
                        processory_price, session
                    )

            else:
                city_id = await city_crud.get_id_by_name(city, session)
                processory_price = {
                    'processory_id': processory_id,
                    'store': store,
                    'city_id': city_id,
                    'price': price
                }
                await processory_price_crud.create(
                        processory_price, session
                    )


async def processory_parse(
        functions: List[tuple], cities_count: int, city: str = 'Москва'
) -> None:
    '''
    Функция сохранения и обновления цен и характеристик
    проецссоров от разных магазинов
    '''
    # processories = [
    #     ('AMD Athlon 3000G',
    #      '22212',
    #      'https://www.dns-shop.ru/product/0e189711fb76ed20/processor-amd-athlon-3000g-oem/'
    #      )
    # ]
    available_characteristics, get_products_name_price_link, get_processory_info = functions  # noqa
    processories = get_products_name_price_link(city)

    for processory in processories:

        name, price, link = processory
        store = link.split('/')[2]

        async with AsyncSessionLocal() as session:

            link_id = await parsed_site_crud.get_id_by_url(link, session)
            is_site_already_parsed = await parsed_site_crud.get(
                link_id, session
            )
            processory_id = await processory_crud.get_id_by_name(
                    name, session
                )
            processory = await check_processory_exists(
                    processory_id, session
                )

            if not is_site_already_parsed:

                if processory is not None:
                    none_fields = (
                        await processory_crud.get_processory_blank_fields(
                            name, session
                        )
                    )
                    if any(map(lambda element: element in none_fields,
                               # CHARACTERISTICS_FROM_DNS
                               available_characteristics
                               )):
                        processory_info = get_processory_info(link)
                        # processory_info = get_dns_processory_info(link)
                        await processory_crud.update(
                            processory, processory_info, session
                        )

                else:
                    processory_info = get_processory_info(link)
                    # processory_info = get_dns_processory_info(link)
                    processory = await processory_crud.create(
                        processory_info, session
                    )
                    processory_id = processory.id

                await parsed_site_crud.create(
                    obj_in={'url': link}, session=session
                )
            await create_update_processory_price(
                processory_id, store, price, cities_count, city
            )


# def main():
#     '''Главная функция. Зпускает парсинг товаров и их цен'''
#     cities = asyncio.run(get_cities())
#     cities_count = len(cities)
#     for city in cities:
#         for functions in FUNCTIONS_DEPEND_ON_REGION:
#             asyncio.run(processory_parse(functions, cities_count, city))

#     for functions in FUNCTIONS_NOT_DEPEND_ON_REGION:
#         asyncio.run(processory_parse(functions, cities_count))


async def main():
    '''Главная функция. Зпускает парсинг товаров и их цен'''
    # cities = await get_cities()
    cities = ['Абакан', 'Москва']
    cities_count = len(cities)
    tasks = []
    for city in cities:
        for functions in FUNCTIONS_DEPEND_ON_REGION:
            # asyncio.run(processory_parse(functions, cities_count, city))
            tasks.append(processory_parse(functions, cities_count, city))

    await asyncio.gather(*tasks)

    # for functions in FUNCTIONS_NOT_DEPEND_ON_REGION:
    #     # asyncio.run(processory_parse(functions, cities_count))
    #     print(functions, cities_count)


if __name__ == '__main__':
    # cities = asyncio.run(get_cities())
    # for city in cities:
    #     asyncio.run(processory_parse(city))

    # main()

    asyncio.run(main())

    # asyncio.run(create_update_processory_price(
    #     processory_id=4, store='www.regard.ru', price='99',
    #     cities_count=170, city='Москва'
    # ))
