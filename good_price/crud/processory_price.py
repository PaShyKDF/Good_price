from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi.encoders import jsonable_encoder

from good_price.crud.base import CRUDBase
from good_price.models import ProcessoryPrice, User


class CRUDProcessoryPrice(CRUDBase):
    async def create(
            self,
            obj_in,
            session: AsyncSession,
            # processory_id: int,
            # city_id: int,
            user: Optional[User] = None,
    ):
        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict()
        if user is not None:
            obj_in['user_id'] = user.id
        # obj_in['processory_id'] = processory_id
        # obj_in['city_id'] = city_id
        db_obj = ProcessoryPrice(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def multiple_update(
            self,
            db_objs,
            obj_in,
            session: AsyncSession,
    ):
        for db_obj in db_objs:
            obj_data = jsonable_encoder(db_obj)
            if not isinstance(obj_in, dict):
                update_data = obj_in.dict(exclude_unset=True)
            else:
                update_data = obj_in

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            session.add(db_obj)

        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_processory_price(
            self,
            processory_id: int,
            store: str,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(ProcessoryPrice).where(
                and_(
                    ProcessoryPrice.processory_id == processory_id,
                    ProcessoryPrice.store == store
                )
            )
        )
        return db_obj.scalars().first()

    async def get_processory_prices(
            self,
            processory_id: int,
            store: str,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(ProcessoryPrice).where(
                and_(
                    ProcessoryPrice.processory_id == processory_id,
                    ProcessoryPrice.store == store
                )
            )
        )
        return db_obj.scalars().all()


processory_price_crud = CRUDProcessoryPrice(ProcessoryPrice)
