"""..."""

from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import db_manager
from schemas.agent import ChatRequest
from services.agent import agent_service


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/")
def chat(
    chat_request: ChatRequest,
    db: Session = Depends(db_manager.get_db),
):
    return agent_service.chat(
        question=chat_request.question,
        db=db,
        user_id=chat_request.user_id,
        session_id=chat_request.session_id,
        file_name=chat_request.file_name,
        storage_uri=chat_request.storage_uri,
        dataset_summary=chat_request.dataset_summary,
    )
