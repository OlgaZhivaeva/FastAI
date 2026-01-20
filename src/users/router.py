from fastapi import APIRouter

from .schemas import UserDetailsResponse
from .service import mock_get_user

users_router = APIRouter(prefix="/frontend-api/users", tags=["Users"])


@users_router.get(
    "/me",
    summary="Получить данные пользователя",
    response_description="Данные пользователя",
    response_model=UserDetailsResponse,
)
async def get_user():
    return mock_get_user()
