"""..."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.v1.router import api_router
from core.db import db_manager
from core.session_cache import session_cache
from models.base import Base

Base.metadata.create_all(bind=db_manager.engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_cache.connect_client()
    yield
    session_cache.close_client()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
