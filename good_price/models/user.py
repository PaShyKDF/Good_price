from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from good_price.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
