from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_data() -> dict[str, str]:
    return {"greeting": "Hello World!!"}
