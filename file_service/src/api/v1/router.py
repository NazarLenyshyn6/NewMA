"""..."""

from fastapi import APIRouter

from api.v1.routes.file import router as file_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(file_router)
