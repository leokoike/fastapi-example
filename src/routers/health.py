from http import HTTPStatus
from fastapi import APIRouter

router = APIRouter()


@router.get("/", status_code=HTTPStatus.OK)
async def read_root() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health", status_code=HTTPStatus.OK)
async def health() -> dict[str, bool]:
    return {"status": "ok"}
