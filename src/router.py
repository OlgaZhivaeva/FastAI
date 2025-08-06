from starlette.responses import HTMLResponse

# from starlette.staticfiles import StaticFiles
# from main import FRONTEND_DIR, app
from main import api_router
from views.create_site import CreateSiteResponse, mock_create_site
from views.generate_html import mock_generate_html
from views.get_site import SiteResponse, mock_get_site
from views.get_user import UserDetailsResponse, mock_get_user
from views.get_user_sites import GeneratedSitesResponse, mock_get_user_sites

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
)(mock_get_user_sites)


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
    response_model=CreateSiteResponse,
)(mock_create_site)


api_router.post(
    "/sites/{site_id}/generate",
    summary="Сгенерировать HTML код сайта",
    response_description="HTML код сайта",
    tags=["Sites"],
    response_class=HTMLResponse,
)(mock_generate_html)
