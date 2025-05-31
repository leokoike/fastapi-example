from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    tvshows: list["UserTVShow"] = []


class TVShow(BaseModel):
    id: int
    title: str
    genre: str
    year: int

    users: list["UserTVShow"] = []


class UserTVShow(BaseModel):
    user: User | None = None
    tvshow: TVShow | None = None
    rating: int
    added_at: datetime
