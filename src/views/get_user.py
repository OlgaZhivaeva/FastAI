from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, PastDatetime, StringConstraints

from reuseble_types import response_config_dict


class UserDetailsResponse(BaseModel):
    profile_id: int
    """Уникальный идентификатор профиля пользователя"""
    email: EmailStr
    """Электронный адрес пользователя для связи и уведомлений"""
    username: Annotated[str, StringConstraints(max_length=254)]
    """Имя пользователя для входа в систему и идентификации"""
    registered_at: Annotated[datetime, PastDatetime]
    """Дата регистрации пользователя в системе"""
    updated_at: Annotated[datetime, PastDatetime]
    """Дата последнего обновления профиля пользователя"""
    is_active: bool
    """Флаг, указывающий, активен ли профиль пользователя"""

    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "profile_id": 123,
                "email": "IIvanov@mail.ru",
                "username": "Иван",
                "registered_at": "2024-01-01T00:00:00",
                "updated_at": "2025-01-08T00:00:00",
                "is_active": False,
            },
        },
    )


def mock_get_user():
    """/frontend-api/users/me"""
    return {
        "profile_id": 1,
        "email": "IIvanov@mail.ru",
        "username": "Иван",
        "registered_at": "2025-01-01T12:00:00",
        "updated_at": "2025-01-01T00:00:00",
        "is_active": True,
    }
