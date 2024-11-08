from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    '''Настройки проекта'''

    app_title: str = 'Good Price'
    description: str = 'Сервис сравнения цен на компьютерные комплектующие'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
