"""..."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.v1.router import api_router
from core.db import db_manager

from cache.memory import (
    conversation_summary_memory_cache,
    conversation_memory_cache,
    code_summary_memory_cache,
    variables_memory_cache,
)
from models.memory import BaseMemory

BaseMemory.metadata.create_all(bind=db_manager.engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    cache_managers = [
        conversation_summary_memory_cache,
        conversation_memory_cache,
        code_summary_memory_cache,
        variables_memory_cache,
    ]
    for cache_manager in cache_managers:
        cache_manager.connect_client()
    yield
    for cache_manager in cache_managers:
        cache_manager.close_client()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8005)
