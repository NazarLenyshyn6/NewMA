"""..."""

from uuid import UUID
from typing import Optional


from schemas.base import BaseSchema


class ChatHistory(BaseSchema):
    """..."""

    session_id: UUID
    solutions: Optional[bytes]
    code: Optional[bytes]
    variables: Optional[bytes]
