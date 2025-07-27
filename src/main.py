from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

FRONTEND_DIR = Path(__file__).parent / "frontend"

app = FastAPI()


class UserProfile(BaseModel):
    profile_id: int
    """Уникальный идентификатор профиля пользователя"""
    email: EmailStr
    """Электронный адрес пользователя для связи и уведомлений"""
    username: str
    """Имя пользователя для входа в систему и идентификации"""
    registered_at: datetime
    """Дата регистрации пользователя в системе"""
    updated_at: datetime
    """Дата последнего обновления профиля пользователя"""
    is_active: bool
    """Флаг, указывающий, активен ли профиль пользователя"""

    @field_validator("registered_at", "updated_at")
    def check_date_not_future(cls, value):
        now = datetime.now()
        if value > now:
            raise ValueError("Дата не может быть в будущем")
        return value

    model_config = ConfigDict(
        use_attribute_docstrings=True,
        json_schema_extra={
            "example": {
                "profile_id": 123,
                "email": "IIvanov@mail.ru",
                "username": "Иван",
                "registered_at": "2024-01-01T12:00:00",
                "updated_at": "2025-01-01T00:00:00",
                "is_active": False,
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
def mock_get_user():
    return {
        "profile_id": 1,
        "email": "IIvanov@mail.ru",
        "username": "Иван",
        "registered_at": "2025-01-01T12:00:00",
        "updated_at": "2025-01-01T00:00:00",
        "is_active": True,
    }


app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)
