from src.schemas import TVShowSchema, UserSchema, UserTVShowSchema
from src.data import TVShow, User, UserTVShow

__all__ = [
    "convert_user",
    "convert_tvshow",
    "convert_user_tvshow_from_user",
]


def convert_user(schema: UserSchema, get_tvshows: bool = True) -> User:
    tvshows = []
    if get_tvshows:
        tvshows = (
            [
                convert_user_tvshow_from_user(user_tvshow)
                for user_tvshow in schema.user_tvshows
            ]
            if schema.user_tvshows
            else []
        )
    return User(
        id=schema.id,
        username=schema.username,
        email=schema.email,
        password=schema.password,
        created_at=schema.created_at,
        tvshows=tvshows,
    )


def convert_tvshow(schema: TVShowSchema, get_users: bool = True) -> TVShow:
    users = []
    if get_users:
        users = (
            [
                _convert_user_tvshow_from_tvshow(user_tvshow)
                for user_tvshow in schema.user_tvshows
            ]
            if schema.user_tvshows
            else []
        )

    return TVShow(
        id=schema.id,
        title=schema.title,
        genre=schema.genre,
        year=schema.year,
        users=users,
    )


def convert_user_tvshow_from_user(schema: UserTVShowSchema) -> UserTVShow:
    tvshow = convert_tvshow(
        schema.tvshow,
        get_users=False,
    )
    return UserTVShow(
        user=None,
        tvshow=tvshow,
        rating=schema.rating,
        added_at=schema.added_at,
    )


def _convert_user_tvshow_from_tvshow(schema: UserTVShowSchema) -> UserTVShow:
    user = convert_user(
        schema.user,
        get_tvshows=False,
    )
    return UserTVShow(
        user=user,
        tvshow=None,
        rating=schema.rating,
        added_at=schema.added_at,
    )
