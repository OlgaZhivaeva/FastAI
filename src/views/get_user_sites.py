from pydantic import BaseModel, ConfigDict

from reuseble_types import Site, response_config_dict


class GeneratedSitesResponse(BaseModel):
    sites: list[Site]
    """Список сайтов пользователя"""

    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "created_at": "2025-06-15T18:29:56",
                "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
                "html_code_url": "http://example.com/media/index.html",
                "id": 1,
                "prompt": "Сайт любителей играть в домино",
                "screenshot_url": "http://example.com/media/index.png",
                "title": "Фан клуб Домино",
                "updated_at": "2025-06-15T18:29:56",
            },
        },
    )


def mock_get_user_sites():
    """/frontend-api/users/my"""
    return {
        "sites":
        [
            {
            "created_at": "2025-01-01T00:00:00",
            "html_code_download_url": "src/index.html?response-content-disposition=attachment",
            "html_code_url": "src/index.html",
            "id": 1,
            "prompt": "Сайт садоводов любителей",
            "screenshot_url": "src/index.html",
            "title": "Садоводы любители",
            "updated_at": "2025-01-01T00:00:00",
            },
        ],
    }
