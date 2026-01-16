from fastapi import Request
from pydantic import BaseModel, ConfigDict

from src.reuseble_types import SITE_EXAMPLE, Site, response_config_dict
from src.sites.service import generate_s3_url


class GeneratedSitesResponse(BaseModel):
    sites: list[Site]
    """Список сайтов пользователя"""

    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                "sites": [
                    {
                        "createdAt": "2025-06-15T18:29:56",
                        "htmlCodeDownloadUrl": "http://example.com/media/index.html?response-content-disposition=attachment",
                        "htmlCodeUrl": "http://example.com/media/index.html",
                        "id": 1,
                        "prompt": "Сайт любителей играть в домино",
                        "screenshotUrl": "http://example.com/media/index.png",
                        "title": "Фан клуб Домино",
                        "updatedAt": "2025-06-15T18:29:56",
                    },
                ],
            },
        },
    )


def mock_get_user_sites(http_request: Request):
    """get /frontend-api/sites/my"""
    settings_s3 = http_request.app.state.settings.s3

    return {
        "sites":
        [
            {
                **SITE_EXAMPLE,
                "html_code_download_url": generate_s3_url(settings_s3, disposition="attachment"),
                "html_code_url": generate_s3_url(settings_s3, disposition="inline"),
                "screenshot_url": generate_s3_url(settings_s3, file_name="index.png"),
            },
        ],
    }
