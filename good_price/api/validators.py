from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from good_price.crud.city import city_crud
from good_price.models import City


async def check_city_name_duplicate(
        city_name: str,
        session: AsyncSession,
) -> None:
    '''Проверка названия города на уникальность'''
    charity_project_id = await city_crud.get_id_by_name(
        city_name, session
    )

    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Такой город уже существует!',
        )


async def check_city_exists(
        city_id: int,
        session: AsyncSession,
) -> City:
    city = await city_crud.get(
        city_id, session
    )

    if city is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Город не найден!'
        )
    return city
