from sqlalchemy import Column, String, Integer, Float, CheckConstraint

from good_price.core.db import Base


class Processory(Base):
    '''Таблица хранящая все характеристики группы процессоров'''

    # __abstract__ = True
    __table_args__ = (
        CheckConstraint('2 < tech_process <= 65'),
        # CheckConstraint('invested_amount <= full_amount'),
    )

    name = Column(String(150), unique=True, nullable=False)
    lineup = Column(String(20))  # Линейка - i7, i5, ryzen 7
    socket = Column(String(15), nullable=False)
    tech_process = Column(String(6))
    equipment = Column(String(3), nullable=False)  # Комплектация - OEM или BOX

    clock_frequency = Column(Float)
    turboboost_frequency = Column(Float)
    cores_amount = Column(Integer)
    productive_cores_amount = Column(Integer)
    energy_efficient_cores_amount = Column(Integer)
    threads_amount = Column(Integer)
    tdp = Column(String(6))
    second_level_cache = Column(String(10))
    third_level_cache = Column(String(10))
    free_multiplier = Column(String(3))
    RAM_support = Column(String(4))  # DDR3, DDR4, DDR5
    graphics_core = Column(String(4))
