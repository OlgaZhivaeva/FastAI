import asyncio
from collections.abc import AsyncGenerator
from itertools import count

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI()


@app.get("/")
async def get_data() -> dict[str, str]:
    return {"greeting": "Hello World!!"}


async def generate_counter() -> AsyncGenerator[str, None]:
    for number in count():
        yield f"<h1>{number}\n</h1>"
        await asyncio.sleep(1)


@app.get("/counter", response_class=HTMLResponse)
async def stream_counter() -> StreamingResponse:
    return StreamingResponse(
        generate_counter(),
        media_type="text/html",
    )
