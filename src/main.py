from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from router import api_router
from settings import AppSettings

FRONTEND_DIR = Path(__file__).parent / "frontend"

settings = AppSettings()

print("Настройки приложения:", settings.model_dump_json(indent=4))


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings
    app.include_router(api_router)

    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="frontend",
    )
    yield


app = FastAPI(lifespan=lifespan)
