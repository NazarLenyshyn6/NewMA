"""..."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from core.db import db_manager
from schemas.agent import ChatRequest


from services.agent import AgentService


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/stream")
async def chat_stream(
    chat_request: ChatRequest,
    db: Session = Depends(db_manager.get_db),
):
    stream = AgentService.chat_stream(
        question=chat_request.question,
        db=db,
        user_id=chat_request.user_id,
        session_id=chat_request.session_id,
        file_name=chat_request.file_name,
        storage_uri=chat_request.storage_uri,
        dataset_summary=chat_request.dataset_summary,
    )
    return StreamingResponse(stream, media_type="text/event-stream")
