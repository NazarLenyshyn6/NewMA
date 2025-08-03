"""..."""

from uuid import UUID
from typing import Optional


from schemas.base import BaseSchema


class ChatHistory(BaseSchema):
    """..."""

    user_id: int
    session_id: UUID
    file_name: str
    solutions: Optional[bytes]
    code: Optional[bytes]
    variables: Optional[bytes]
