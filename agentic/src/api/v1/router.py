"""..."""

from fastapi import APIRouter

from api.v1.routes.agent import router as agent_router
from api.v1.routes.memory import router as memory_router

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(memory_router)
api_router.include_router(agent_router)
