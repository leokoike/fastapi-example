from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from db import get_session
from schemas import TVShowSchema, UserSchema, UserTVShowSchema
from data import TVShow, User
from converter import convert_tvshow, convert_user

router = APIRouter()


@router.get("/users", response_model=Page[User])
async def list_users(session: Session = Depends(get_session)):
    """
    List all users with pagination.
    """
    users = (
        session.execute(select(UserSchema).order_by(UserSchema.username))
        .scalars()
        .all()
    )

    data = [convert_user(user, get_tvshows=False) for user in users]

    return paginate(data)


@router.get("users/{user_id}/tvshows", response_model=Page[TVShow])
async def get_user_tvshows(user_id: int, session: Session = Depends(get_session)):
    """
    Get all TV shows that belong to a specific user.
    """
    tv_shows = (
        session.execute(
            select(TVShowSchema)
            .join(UserTVShowSchema, TVShowSchema.id == UserTVShowSchema.id)
            .join(UserSchema, UserTVShowSchema.user_id == UserSchema.id)
            .where(UserSchema.id == user_id)
            .order_by(TVShowSchema.title)
        )
        .scalars()
        .all()
    )
    if not tv_shows:
        raise HTTPException(status_code=404, detail="User not found")

    data = [convert_tvshow(tv_show, get_users=False) for tv_show in tv_shows]
    return paginate(data)
