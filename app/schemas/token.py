"""..."""

from typing import Optional

from pydantic import EmailStr

from app.schemas.base import BaseSchema


class Token(BaseSchema):
    """..."""

    access_token: str
    token_type: str


class TokenData(BaseSchema):
    """..."""

    email: Optional[EmailStr] = None
