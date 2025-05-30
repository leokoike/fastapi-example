from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from sqlalchemy import select

from db import get_session
from schemas import TVShowSchema
from data import TVShow
from src.converter import convert_tvshow

router = APIRouter()


@router.get("/tvshows", response_model=Page[TVShow])
async def get_tvshows(
    session: Session = Depends(get_session),
) -> Page[TVShow]:
    """
    Retrieve a paginated list of TV shows.
    """
    tvshows = (
        session.execute(select(TVShowSchema).order_by(TVShowSchema.title))
        .scalars()
        .all()
    )
    if not tvshows:
        raise HTTPException(status_code=404, detail="No TV shows found")

    data = [convert_tvshow(tvshow) for tvshow in tvshows]

    return paginate(data)
