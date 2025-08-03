"""..."""

from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    user_id: int
    session_id: UUID
    file_name: str
    storage_uri: str
