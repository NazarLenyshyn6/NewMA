"""
This module defines FastAPI routes related to AI agent interactions.
It provides endpoints for streaming agent responses in real-time,
integrating with the database session and the `AgentRequest` schema.

Routes:
    POST /agent/stream : Streams the AI agent's response to a user query.
"""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse


from core.db import db_manager
from schemas.agent import AgentRequest
from services.agent import agent_service

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/stream")
async def stream(
    agent_request: AgentRequest,
    db: Session = Depends(db_manager.get_db),
):
    """
    Streams the AI agent's response to a user query using Server-Sent Events (SSE).

    This endpoint takes an `AgentRequest` containing the user's question and metadata,
    initializes the agent service stream, and returns a StreamingResponse so that
    the client can receive partial outputs in real-time as the agent generates them.

    Args:
        agent_request: The user request containing:
            - question: The question to ask the AI agent.
            - user_id: Unique ID of the user.
            - session_id: Session ID for tracking.
            - file_name: Associated file name, if applicable.
            - storage_uri: Storage location URI for related data.
            - dataset_summary: Summary of the dataset context.
        db (Session, optional): SQLAlchemy database session provided via dependency injection.

    Returns:
        StreamingResponse: A streaming HTTP response that sends text/event-stream
        data as the AI agent generates its answer.
    """
    stream = agent_service.stream(
        question=agent_request.question,
        db=db,
        user_id=agent_request.user_id,
        file_name=agent_request.file_name,
        session_id=agent_request.session_id,
        storage_uri=agent_request.storage_uri,
        dataset_summary=agent_request.dataset_summary,
    )

    return StreamingResponse(stream, media_type="text/event-stream")
