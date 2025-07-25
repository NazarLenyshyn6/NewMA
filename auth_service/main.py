"""..."""

import uvicorn
from fastapi import FastAPI

from api.v1.router import api_router
from core.db import db_manager
from models.base import Base

Base.metadata.create_all(bind=db_manager.engine)

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
