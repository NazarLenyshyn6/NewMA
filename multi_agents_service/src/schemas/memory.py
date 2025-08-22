"""..."""

from uuid import UUID
from typing import Optional

from pydantic import BaseModel


class BaseMemory(BaseModel):
    """..."""

    model_config = {"from_attributes": True}

    user_id: int
    session_id: UUID
    file_name: str
    memory: Optional[bytes] = None


class ConversationSummaryMemory(BaseMemory): ...


class ConversationMemory(BaseMemory): ...


class CodeSummaryMemory(BaseMemory): ...


class VariablesMemory(BaseMemory): ...


class MemorySave(BaseMemory): ...
