"""..."""

from fastapi import APIRouter

from api.v1.routes.auth import router as auth_router
from api.v1.routes.session import router as session_router
from api.v1.routes.file import router as file_router
from api.v1.routes.chat import router as chat_router

api_router = APIRouter(prefix="/api/v1/gateway")

api_router.include_router(auth_router)
api_router.include_router(session_router)
api_router.include_router(file_router)
api_router.include_router(chat_router)
