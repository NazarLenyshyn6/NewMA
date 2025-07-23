"""..."""

from typing import Optional


from app.schemas.base import BaseSchema


class Token(BaseSchema):
    """..."""

    access_token: str
    token_type: str


class TokenData(BaseSchema):
    """..."""

    id: Optional[str] = None
