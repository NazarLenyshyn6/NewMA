"""..."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from clients.session import SessionClient
from clients.file import FileClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/gateway/auth/login")

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/")
def chat(question: str, token: str = Depends(oauth2_scheme)):
    actvice_session = SessionClient.get_active_session_id(token=token)
    active_file = FileClient.get_active_file(token=token, session=actvice_session)
    return {
        "mocked answer": "Hello :)",
        "user_questoin": question,
        "active_session": actvice_session,
        "active_file": active_file,
    }
