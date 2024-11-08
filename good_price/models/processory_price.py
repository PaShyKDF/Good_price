from sqlalchemy import Column, String, Integer, ForeignKey  # ,UniqueConstraint

from good_price.core.db import Base


class ProcessoryPrice(Base):
    '''Таблица цен на процессоры в разных городах'''

    # __table_args__ = (
    #     UniqueConstraint('store', 'city_id', name='_store_city_uc'),
    # )

    processory_id = Column(
        Integer, ForeignKey('processory.id'), nullable=False
    )
    store = Column(String, nullable=False)
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)
    price = Column(Integer, nullable=False)
