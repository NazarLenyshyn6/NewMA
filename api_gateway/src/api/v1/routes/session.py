"""..."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from schemas.session import NewSessionRequest
from clients.session import SessionClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/gateway/auth/login")

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get("/")
def get_session(token: str = Depends(oauth2_scheme)):
    return SessionClient.get_sessions(token=token)


@router.get("/active")
def get_active_session_id(token: str = Depends(oauth2_scheme)):
    return SessionClient.get_active_session_id(token=token)


@router.post("/")
def create_session(new_session: NewSessionRequest, token: str = Depends(oauth2_scheme)):
    return SessionClient.create_session(token=token, title=new_session.title)


@router.post("/active/{title}")
def set_active_session(title: str, token: str = Depends(oauth2_scheme)):
    return SessionClient.set_active_session(token=token, title=title)


@router.delete("/{title}")
def delete_session(title: str, token: str = Depends(oauth2_scheme)):
    return SessionClient.delete_session(token=token, title=title)
