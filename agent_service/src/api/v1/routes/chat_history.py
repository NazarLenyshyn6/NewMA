"""..."""

from uuid import UUID


from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import db_manager
from services.chat_history import chat_history_service

router = APIRouter(prefix="/chat_history", tags=["ChatHistory"])

from pydantic import BaseModel


class ChatHistoryRead(BaseModel):
    user_id: int
    session_id: UUID
    file_name: str


@router.get("/", response_model=ChatHistoryRead)
def get_chat_history(
    user_id: int,
    session_id: UUID,
    file_name: str,
    storage_uri: str,
    db: Session = Depends(db_manager.get_db),
):
    """..."""
    return chat_history_service.get_chat_history(
        db=db,
        user_id=user_id,
        session_id=session_id,
        file_name=file_name,
        storage_uri=storage_uri,
    )


@router.delete("/")
def delete_chat_history(
    user_id: int,
    file_name: str,
    db: Session = Depends(db_manager.get_db),
):
    chat_history_service.delete_chat_history(
        db=db, user_id=user_id, file_name=file_name
    )
