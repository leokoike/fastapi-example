from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi_pagination import Page, paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.authentication import authenticate
from src.db import get_session
from src.schemas import UserSchema, UserTVShowSchema
from src.data import User, UserTVShow
from src.converter import convert_user, convert_user_tvshow_from_user
from fastapi_pagination.utils import disable_installed_extensions_check

disable_installed_extensions_check()
router = APIRouter()


@router.get(
    "/users",
    response_model=Page[User],
    description="List all users with pagination.",
)
async def list_users(
    username: str = Query(
        None, description="Filter users by username (case-insensitive)"
    ),
    email: str = Query(
        None,
        description="Filter users by email (case-insensitive)",
    ),
    session: Session = Depends(get_session),
    _=Depends(authenticate),
):
    """
    List all users with pagination.
    """
    filters = []
    stmt = select(UserSchema)
    if username:
        filters.append(UserSchema.username.ilike(f"%{username}%"))
    if email:
        filters.append(UserSchema.email.ilike(f"%{email}%"))
    if filters:
        stmt = stmt.where(*filters)

    users = session.execute(stmt.order_by(UserSchema.username)).scalars().all()

    data = [convert_user(user, get_tvshows=False) for user in users]

    return paginate(data)


@router.get(
    "/users/{user_id}/tvshows",
    response_model=Page[UserTVShow],
    description="Get all rated TV shows to a specific user.",
)
async def get_user_tvshows(
    user_id: str,
    session: Session = Depends(get_session),
    _=Depends(authenticate),
):
    """
    Get all TV shows that belong to a specific user.
    """
    user_id = int(user_id)
    user_tv_shows = (
        session.execute(
            select(UserTVShowSchema)
            .join(UserSchema, UserTVShowSchema.user_id == UserSchema.id)
            .where(UserSchema.id == user_id)
            .order_by(UserTVShowSchema.tvshow_id)
        )
        .scalars()
        .all()
    )
    if not user_tv_shows:
        raise HTTPException(status_code=404, detail="User not found")

    data = [
        convert_user_tvshow_from_user(user_tv_show) for user_tv_show in user_tv_shows
    ]
    return paginate(data)
