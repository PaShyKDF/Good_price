from sqlalchemy import Column, String

from good_price.core.db import Base


class City(Base):
    '''Таблица городов России'''

    name = Column(String(25), unique=True, nullable=False)
    country = Column(String(15), nullable=False)
