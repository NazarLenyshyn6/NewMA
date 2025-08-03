"""..."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from clients.session import SessionClient
from clients.file import FileClient
from clients.agent import AgentClient
from core.security import get_current_user_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/gateway/auth/login")

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/")
def chat(
    question: str,
    token: str = Depends(oauth2_scheme),
):
    user_id = get_current_user_id(token)
    session_id = SessionClient.get_active_session_id(token=token)
    active_file = FileClient.get_active_file(token=token, session=session_id)
    response = AgentClient.chat(
        question=question,
        user_id=user_id,
        session_id=session_id,
        file_name=active_file["file_name"],
        storage_uri=active_file["storage_uri"],
    )
    return response
