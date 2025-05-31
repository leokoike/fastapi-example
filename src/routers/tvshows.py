from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.db import get_session
from src.schemas import TVShowSchema
from src.data import TVShow
from src.converter import convert_tvshow

router = APIRouter()


@router.get(
    "/tvshows",
    response_model=Page[TVShow],
    description="Retrieve a paginated list of TV shows containing information of users rating.",
)
async def get_tvshows(
    year_le: int = Query(
        None, description="TV Show year less than or equal to this value"
    ),
    year_ge: int = Query(
        None, description="TV Show year greater than or equal to this value"
    ),
    genre: str = Query(
        None, description="TV Show genre Filter by  (e.g., 'Drama', 'Comedy')"
    ),
    session: Session = Depends(get_session),
) -> Page[TVShow]:
    """
    Retrieve a paginated list of TV shows.
    """
    filters = []
    stmt = select(TVShowSchema)
    if year_le is not None and year_ge is not None:
        filters.append(TVShowSchema.year.between(year_ge, year_le))
    elif year_le is not None:
        filters.append(TVShowSchema.year < year_le)
    elif year_ge is not None:
        filters.append(TVShowSchema.year > year_ge)

    if genre:
        filters.append(TVShowSchema.genre.ilike(f"%{genre}%"))

    if filters:
        stmt = stmt.where(*filters)

    tvshows = session.execute(stmt.order_by(TVShowSchema.title)).scalars().all()
    if not tvshows:
        raise HTTPException(status_code=404, detail="No TV shows found")

    data = [convert_tvshow(tvshow) for tvshow in tvshows]

    return paginate(data)
