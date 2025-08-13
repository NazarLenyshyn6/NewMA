"""..."""

"""..."""

from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from schemas.base import BaseSchema


class AgentMemory(BaseSchema):
    """..."""

    user_id: int
    session_id: UUID
    file_name: str
    conversation_context: Optional[bytes]
    conversation_history: Optional[bytes]
    persisted_variables: Optional[bytes]
    code_context: Optional[bytes]


class AgentMemorySave(BaseModel):
    user_id: int
    session_id: UUID
    file_name: str
