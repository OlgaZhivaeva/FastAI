from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from router import api_router

FRONTEND_DIR = Path(__file__).parent / "frontend"


app = FastAPI()

app.include_router(api_router)

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)
