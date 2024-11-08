from fastapi import APIRouter

from good_price.api.endpoints import (
    city_router,
    # reservation_router,
    user_router,
)

main_router = APIRouter()
main_router.include_router(
    city_router, prefix='/city', tags=['City']
)
# main_router.include_router(
#     reservation_router, prefix='/reservations', tags=['Reservations']
# )

main_router.include_router(user_router)
