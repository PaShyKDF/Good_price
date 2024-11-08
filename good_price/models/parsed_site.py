from datetime import datetime

from sqlalchemy import Column, String, DateTime

from good_price.core.db import Base


class ParsedSite(Base):
    '''Таблица отслеживания парсинга сайтов'''

    url = Column(String, unique=True, nullable=False)
    last_parsed = Column(DateTime, default=datetime.now)
