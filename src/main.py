from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

FRONTEND_DIR = Path(__file__).parent / "frontend"
STATIC_FILES_DIR = Path(__file__).parent / "static"

app = FastAPI()


class UserProfile(BaseModel):
    profile_id: int = Field(..., description="Уникальный идентификатор профиля пользователя")
    email: str = Field(..., description="Электронный адрес пользователя для связи и уведомлений")
    username: str = Field(..., description="Имя пользователя для входа в систему и идентификации")
    registered_at: str = Field(..., description="Дата регистрации пользователя в системе")
    updated_at: str = Field(..., description="Дата последнего обновления профиля пользователя")
    is_active: bool = Field(..., description="Флаг, указывающий, активен ли профиль пользователя")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "profile_id": 123,
                "email": "test@example.com",
                "username": "testuser",
                "registered_at": "2025-01-01",
                "updated_at": "2025-01-01",
                "is_active": True,
            },
        },
    )


@app.get(
    "/frontend-api/users/me",
    summary="Получить данные пользователя",
    response_description="Данные пользователя",
    tags=["Users"],
    response_model=UserProfile,
)
def mock_get_user() -> UserProfile:
    mock_user_data = UserProfile(
        profile_id=1,
        email="IIvanov@example.com",
        username="Иван",
        registered_at="2025-07-01",
        updated_at="2025-07-01",
        is_active=True,
    )
    return mock_user_data


app.mount(
    "/static",
    StaticFiles(directory=STATIC_FILES_DIR),
    name="static-files",
)

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)
