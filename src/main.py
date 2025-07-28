import asyncio
from pathlib import Path

import aiofiles
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from models import SiteRequest, SiteResponse, UserProfile

FRONTEND_DIR = Path(__file__).parent / "frontend"

app = FastAPI()


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


@app.get(
    "/frontend-api/sites/{site_id}",
    summary="Получить сайт",
    response_description="Данные сайта",
    tags=["Sites"],
    response_model=SiteResponse,
)
def mock_get_site(site_id: int):
    return {
        "created_at": "2025-06-15T18:29:56+00:00",
        "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
        "html_code_url": "http://example.com/media/index.html",
        "id": site_id,
        "prompt": "Сайт любителей играть в домино",
        "screenshot_url": "http://example.com/media/index.png",
        "title": "Фан клуб Домино",
        "updated_at": "2025-06-15T18:29:56+00:00",
    }


@app.post(
    "/frontend-api/sites/create",
    summary="Создать сайт",
    response_description="Данные для генерации сайта",
    tags=["Sites"],
    response_model=SiteResponse,
)
def mock_create_site(site: SiteRequest):
    return {
        "created_at": "2025-01-01T12:00:00",
        "html_code_download_url": "http://example.com/media/index.html?response-content-disposition=attachment",
        "html_code_url": "http://example.com/media/index.html",
        "id": 1,
        "prompt": site.prompt,
        "screenshot_url": "http://example.com/media/index.png",
        "title": site.title,
        "updated_at": "2025-01-01T12:00:00",
    }


@app.post(
    "/frontend-api/sites/{site_id}/generate",
    summary="Сгенерировать HTML код сайта",
    response_description="HTML код сайта",
    tags=["Sites"],
    response_class=HTMLResponse,

)
async def mock_generate_html(site_id: int):
    async def html_generator():
        async with aiofiles.open("src/index.html", "rb") as f:
            while True:
                chunk = await f.read(1024)
                if not chunk:
                    break
                yield chunk
                await asyncio.sleep(1)

    return StreamingResponse(html_generator(), media_type="text/html")


app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)
