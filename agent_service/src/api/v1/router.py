"""..."""

from fastapi import APIRouter

# from api.v1.routes.agent import router as agent_router
from api.v1.routes.chat_history import router as chat_history_router

api_router = APIRouter(prefix="/api/v1")

# api_router.include_router(agent_router)
api_router.include_router(chat_history_router)
