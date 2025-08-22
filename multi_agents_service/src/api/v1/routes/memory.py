"""..."""

from uuid import UUID
from typing import List
import pickle

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import db_manager
from services.memory.base import BaseMemoryService
from services.memory.conversation_summary import conversation_summary_memory_service
from services.memory.conversation import conversation_memory_service
from services.memory.code_summary import code_summary_memory_service
from services.memory.variables import variables_memory_service
from schemas.memory import MemorySave

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
    return pickle.loads(
        conversation_memory_service.get_memory(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        ).memory
    )


@router.post("/")
def save_chat_history(
    chat_history_save: MemorySave,
    db: Session = Depends(db_manager.get_db),
):
    memory_services: List[BaseMemoryService] = [
        conversation_summary_memory_service,
        conversation_memory_service,
        code_summary_memory_service,
        variables_memory_service,
    ]
    for memory_service in memory_services:
        memory_service.save_memory(
            db=db,
            user_id=chat_history_save.user_id,
            session_id=chat_history_save.session_id,
            file_name=chat_history_save.file_name,
        )
