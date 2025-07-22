"""..."""

from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema


class UserCreate(BaseSchema):
    """...."""

    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseSchema):
    """..."""

    id: int
    email: EmailStr
    created_at: datetime


class UserInDB(BaseSchema):
    """..."""

    hashed_password: str
