from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from good_price.core.db import get_async_session
from good_price.analitic.city_list import get_cities
from good_price.crud.city import city_crud
from good_price.core.user import current_superuser
from good_price.schemas.city import CityUpdate, CityDB, CityCreate
from good_price.api.validators import (
    check_city_name_duplicate, check_city_exists
)


ADD_CITIES = ('Все города с населением более 100.000 '
              'человек добавлены в базу данных')

router = APIRouter()


@router.post('/add_multi',
             dependencies=[Depends(current_superuser)],
             #  response_model=DonationDB,
             #  response_model_exclude=EXCLUDE_FIELDS
             )
async def create_cities(
    session: AsyncSession = Depends(get_async_session)
) -> str:
    '''
    Только для суперпользователей\n
    Автоматически добавляет в базу данных города России
    с населением более 100.000 человек
    '''

    cities_list = get_cities()
    await city_crud.create_cities(
        cities=cities_list, session=session
    )
    return ADD_CITIES


@router.post('/',
             dependencies=[Depends(current_superuser)],
             response_model=CityDB
             )
async def create_new_city(
        city: CityCreate,
        session: AsyncSession = Depends(get_async_session)
):
    '''
    Только для суперюзеров\n
    Добавить новый город
    '''
    await check_city_name_duplicate(city.name, session)

    return await city_crud.create(city, session)


@router.get('/',
            response_model=List[CityDB])
async def get_all_cities(
    session: AsyncSession = Depends(get_async_session)
):
    '''Получить все города'''
    return await city_crud.get_multi(session)


@router.patch(
    '/{city_id}',
    response_model=CityDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_city(
        city_id: int,
        obj_in: CityUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперпользователей\n
    Изменить запись о городе
    """

    city = await check_city_exists(
        city_id, session
    )

    if obj_in.name is not None:
        await check_city_name_duplicate(obj_in.name, session)

    return await city_crud.update(
        city, obj_in, session
    )


@router.delete(
    '/{city_id}',
    response_model=CityDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_city(
        city_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    '''
    Только для суперюзеров\n
    Удалить город
    '''
    city = await check_city_exists(
        city_id, session
    )

    return await city_crud.remove(
        city, session
    )
