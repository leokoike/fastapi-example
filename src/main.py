from fastapi import FastAPI
from fastapi_pagination import add_pagination


async def create_app() -> FastAPI:
    app = FastAPI()
    add_pagination(app)
    return app
