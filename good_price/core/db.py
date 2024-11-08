from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from good_price.core.config import settings


class PreBase:
    '''Базовый класс для таблиц БД'''

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    '''Получение асинхронной сессии'''

    async with AsyncSessionLocal() as async_session:
        yield async_session
