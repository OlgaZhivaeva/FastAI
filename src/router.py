from fastapi import APIRouter
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from main import (
    FRONTEND_DIR,
    GeneratedSitesResponse,
    SiteResponse,
    UserDetailsResponse,
    app,
    mock_create_site,
    mock_generate_html,
    mock_get_site,
    mock_get_user,
    mock_get_user_sits,
)

api_router = APIRouter(prefix="/frontend-api")

api_router.get(
    "/users/me",
    summary="Получить данные пользователя",
    response_description="Данные пользователя",
    tags=["Users"],
    response_model=UserDetailsResponse,
)(mock_get_user)


api_router.get(
    "/sites/my",
    summary="Получить список сайтов пользователя",
    response_description="Сайты пользователя",
    tags=["Sites"],
    response_model=GeneratedSitesResponse,
)(mock_get_user_sits)


api_router.get(
    "/sites/{site_id}",
    summary="Получить сайт",
    response_description="Данные сайта",
    tags=["Sites"],
    response_model=SiteResponse,
)(mock_get_site)


api_router.post(
    "/sites/create",
    summary="Создать сайт",
    response_description="Данные для генерации сайта",
    tags=["Sites"],
    response_model=SiteResponse,
)(mock_create_site)


api_router.post(
    "/sites/{site_id}/generate",
    summary="Сгенерировать HTML код сайта",
    response_description="HTML код сайта",
    tags=["Sites"],
    response_class=HTMLResponse,
)(mock_generate_html)

app.include_router(api_router)
app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)
