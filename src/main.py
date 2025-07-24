from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).parent / "frontend"
STATIC_FILES_DIR = Path(__file__).parent / "static"

app = FastAPI()


@app.get(
    "/frontend-api/users/me",
    summary="Получить данные пользователя",
    response_description="Данные пользователя",
    tags=["Users"],
)
def mock_get_user():
    mock_user_data = {
        "profile_id": 1,
        "email": "IIvanov@example.com",
        "username": "Иван",
        "registered_at": "2025-07-01",
        "updated_at": "2025-07-01",
        "is_active": True,
        }
    return mock_user_data


app.mount(
    "/static",
    StaticFiles(directory=STATIC_FILES_DIR),
    name="static-files",
)

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)
