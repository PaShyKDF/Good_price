# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from good_price.crud.processory import processory_crud
# from good_price.schemas.processory import ProcessoryCreate, ProcessoryDB
# from good_price.core.db import get_async_session
# from good_price.api.validators import check_processory_name_duplicate
# from good_price.core.user import current_superuser


# router = APIRouter()


# @router.post('/',
#              dependencies=[Depends(current_superuser)],
#              response_model=ProcessoryDB,
#              response_model_exclude_none=True
#              )
# async def create_new_processory(
#         processory: ProcessoryCreate,
#         session: AsyncSession = Depends(get_async_session)
# ):
#     '''
#     Только для суперпользователей\n
#     Создание процессора в базе данных
#     '''
#     await check_processory_name_duplicate(processory.name, session)

#     return await processory_crud.create(processory, session)
