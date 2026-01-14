from fastapi import Request
from pydantic import ConfigDict

from src.reuseble_types import Site, response_config_dict
from src.sites.service import generate_s3_url


class SiteResponse(Site):
    model_config = response_config_dict | ConfigDict(
        json_schema_extra={
            "example": {
                    "createdAt": "2025-06-15T18:29:56+00:00",
                    "htmlCodeDownloadUrl": "http://example.com/media/index.html?response-content-disposition=attachment",
                    "htmlCodeUrl": "http://example.com/media/index.html",
                    "id": 1,
                    "prompt": "Сайт любителей играть в домино",
                    "screenshotUrl": "http://example.com/media/index.png",
                    "title": "Фан клуб Домино",
                    "updatedAt": "2025-06-15T18:29:56+00:00",
            },
        },
    )


def mock_get_site(site_id: int, http_request: Request):
    """get /frontend-api/sites/{site_id}"""
    settings_s3 = http_request.app.state.settings.s3
    html_code_download_url = generate_s3_url(settings_s3, disposition="attachment")
    html_code_url = generate_s3_url(settings_s3)
    screenshot_url = generate_s3_url(settings_s3, file_name="index.png", disposition="inline")

    return {
        "created_at": "2025-01-01T00:00:00",
        "html_code_download_url": html_code_download_url,
        "html_code_url": html_code_url,
        "id": site_id,
        "prompt": "Промпт пользователя",
        "screenshot_url": screenshot_url,
        "title": "Название сайта",
        "updated_at": "2025-01-01T00:00:00",
    }
