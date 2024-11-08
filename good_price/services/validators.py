from http import HTTPStatus
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from good_price.crud.processory import processory_crud
from good_price.models import Processory


async def check_processory_name_duplicate(
        processory_name: str,
        session: AsyncSession,
) -> None:
    processory_id = await processory_crud.get_id_by_name(
        processory_name, session
    )

    if processory_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_processory_exists(
        processory_id: int,
        session: AsyncSession,
) -> Optional[Processory]:
    processory = await processory_crud.get(
        processory_id, session
    )
    return processory
