from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from src.reuseble_types import SITE_EXAMPLE, request_config_dict


class CreateSiteRequest(BaseModel):
    prompt: str
    """Промпт"""
    title: Annotated[
        str,
        StringConstraints(max_length=254),
    ] | None = "Название сайта"
    """Название сайта"""

    model_config = request_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Сайт любителей космических путешествий",
                "title": "Космический сайт",
            },
        },
    )


def mock_create_site(request: CreateSiteRequest):
    """post /frontend-api/sites/create"""
    return {
        **SITE_EXAMPLE,
        "prompt": request.prompt,
        "title": request.title,
    }
