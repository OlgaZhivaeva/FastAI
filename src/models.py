from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


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


class CreateSiteResponse(BaseModel):
    id: int
    """Уникальный идентификатор сайта"""
    title: str
    """Название сайта"""
    prompt: str
    """Промпт"""
    created_at: datetime
    """Дата создания сайта"""
    updated_at: datetime
    """Дата последнего обновления сайта"""
    html_code_download_url: str
    """ """
    html_code_url: str
    """ """
    screenshot_url: str
    """ """

    model_config = ConfigDict(
        use_attribute_docstrings=True,
        json_schema_extra={
            "example": {
                "created_at": "2025-06-15T18:29:56+00:00",
                "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
                "html_code_url": "http://example.com/media/index.html",
                "id": 1,
                "prompt": "Сайт любителей играть в домино",
                "screenshot_url": "http://example.com/media/index.png",
                "title": "Фан клуб Домино",
                "updated_at": "2025-06-15T18:29:56+00:00",
            },
        },
    )


class SiteRequest(BaseModel):
    prompt: str
    """Промпт"""
    title: str
    """Название сайта"""
