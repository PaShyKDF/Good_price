from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.inspection import inspect

from good_price.crud.base import CRUDBase
from good_price.models import Processory


class CRUDProcessory(CRUDBase):
    # async def create_processors(
    #         self,
    #         processor: Dict[str, Union[str, int]],
    #         session: AsyncSession,
    # ):
    #     '''
    #     Добавление процессора в базу данных
    #     '''

    #     for city in cities:
    #         existing_city = await session.execute(
    #             select(City).where(City.name == city['name'])
    #         )
    #         existing_city = existing_city.scalars().first()
    #         if existing_city:
    #             continue
    #         db_item = City(**city)
    #         session.add(db_item)

    #     if session.new:
    #         session.commit()

    async def get_id_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        '''Возвращает id процессора по его названию'''
        db_project_id = await session.execute(
            select(Processory.id).where(
                Processory.name == name
            )
        )
        return db_project_id.scalars().first()

    async def get_processory_blank_fields(
            self,
            name: str,
            session: AsyncSession,
    ) -> List[str]:
        '''Возвращает список незаполненных полей процессора'''
        result = await session.execute(
            select(Processory).where(
                Processory.name == name
            )
        )
        result = result.scalars().first()
        mapper = inspect(Processory)
        none_fields = []
        for column in mapper.columns:
            value = getattr(result, column.name)
            if value is None:
                none_fields.append(column.name)
        return none_fields


processory_crud = CRUDProcessory(Processory)
