from datetime import datetime
from typing import List
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


__all__ = [
    "Base",
    "UserTVShowSchema",
    "UserSchema",
    "TVShowSchema",
]


class Base(DeclarativeBase):
    pass


class UserTVShowSchema(Base):
    __tablename__ = "user_tvshows"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    tvshow_id: Mapped[int] = mapped_column(
        ForeignKey("tvshows.id"),
    )
    rating: Mapped[int] = mapped_column(Integer)
    added_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )

    user: Mapped["UserSchema"] = relationship(back_populates="user_tvshows")
    tvshow: Mapped["TVShowSchema"] = relationship(back_populates="user_tvshows")


class UserSchema(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )

    user_tvshows: Mapped[List["UserTVShowSchema"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class TVShowSchema(Base):
    __tablename__ = "tvshows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    genre: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer)

    user_tvshows: Mapped[List["UserTVShowSchema"]] = relationship(
        back_populates="tvshow",
        cascade="all, delete-orphan",
    )
