from typing import List, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from good_price.crud.base import CRUDBase
from good_price.models import City


class CRUDCity(CRUDBase):
    async def create_cities(
            self,
            cities: List[Dict[str, str]],
            session: AsyncSession,
    ):
        '''
        Добавление городов в базу данных из списка словарей вида:\n
        [{'name': 'название города', 'country': 'страна'},]
        '''

        for city in cities:
            existing_city = await session.execute(
                select(City).where(City.name == city['name'])
            )
            existing_city = existing_city.scalars().first()
            if existing_city:
                continue
            db_item = City(**city)
            session.add(db_item)

        if session.new:
            await session.commit()

    async def get_id_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        '''Возвращает id города по его названию'''
        db_project_id = await session.execute(
            select(City.id).where(
                City.name == name
            )
        )
        return db_project_id.scalars().first()

    async def get_cities_list(
            self,
            session: AsyncSession
    ) -> List[str]:
        '''Возвращает все города в виде списка'''
        db_cities = await session.execute(
            select(City.name)
        )
        return db_cities.scalars().all()


city_crud = CRUDCity(City)
