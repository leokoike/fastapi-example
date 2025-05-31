from fastapi import FastAPI
from fastapi_pagination import add_pagination


def add_routers(app: FastAPI) -> None:
    from src.routers import users, tvshows

    app.include_router(users.router, tags=["users"])
    app.include_router(tvshows.router, tags=["tvshows"])


def create_app() -> FastAPI:
    app = FastAPI()
    add_pagination(app)
    add_routers(app)
    return app


app = create_app()
