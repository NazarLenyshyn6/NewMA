"""..."""

from fastapi import APIRouter

from api.v1.routes.session import router as session_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(session_router)
