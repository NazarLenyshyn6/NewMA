"""..."""

from uuid import UUID


from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import db_manager
from services.chat_history import chat_history_service

router = APIRouter(prefix="/chat_history", tags=["ChatHistory"])


class ChatHistorySave(BaseModel):
    user_id: int
    session_id: UUID
    file_name: str


@router.get("/")
def get_conversation_history(
    user_id: int,
    session_id: UUID,
    file_name: str,
    storage_uri: str,
    db: Session = Depends(db_manager.get_db),
):
    """..."""
    return chat_history_service.get_conversation_history(
        db=db,
        user_id=user_id,
        session_id=session_id,
        file_name=file_name,
        storage_uri=storage_uri,
    )


@router.post("/")
def save_chat_history(
    chat_history_save: ChatHistorySave,
    db: Session = Depends(db_manager.get_db),
):
    chat_history_service.save_chat_history(
        db=db,
        user_id=chat_history_save.user_id,
        session_id=chat_history_save.session_id,
        file_name=chat_history_save.file_name,
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
