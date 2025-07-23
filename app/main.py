"""..."""

import uvicorn
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.manager import db_manager
from app.models.base import Base


Base.metadata.create_all(bind=db_manager.engine)

app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
