"""..."""

from uuid import UUID


from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import db_manager
from services.memory import agent_memory_service
from schemas.memory import AgentMemorySave

router = APIRouter(prefix="/chat_history", tags=["ChatHistory"])


@router.get("/")
def get_conversation_history(
    user_id: int,
    session_id: UUID,
    file_name: str,
    storage_uri: str,
    db: Session = Depends(db_manager.get_db),
):
    """..."""
    return agent_memory_service.get_conversation_memory(
        db=db,
        user_id=user_id,
        session_id=session_id,
        file_name=file_name,
        storage_uri=storage_uri,
    )


@router.post("/")
def save_chat_history(
    chat_history_save: AgentMemorySave,
    db: Session = Depends(db_manager.get_db),
):
    agent_memory_service.save_memory(
        db=db,
        user_id=chat_history_save.user_id,
        session_id=chat_history_save.session_id,
        file_name=chat_history_save.file_name,
    )
