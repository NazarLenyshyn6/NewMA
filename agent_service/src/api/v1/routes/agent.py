"""..."""

from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import db_manager

# from services.agent import agent_service

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.post("/generate")
def generate_response(
    question: str, session_id: UUID, db: Session = Depends(db_manager.get_db)
):
    return 1
    # return agent_service.invoke(question=question, session_id=session_id, db=db)
