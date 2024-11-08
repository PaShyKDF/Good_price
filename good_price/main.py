from fastapi import FastAPI

from good_price.core.config import settings
from good_price.api.routers import main_router
from good_price.core.init_db import create_first_superuser


app = FastAPI(
    title=settings.app_title, description=settings.description
)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
