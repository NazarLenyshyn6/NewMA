"""..."""

import uvicorn
from fastapi import FastAPI

from app.models import base as models_base
from app.db.manager import db_manager
from app.api.v1.router import api_router

models_base.Base.metadata.create_all(bind=db_manager.engine)


app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
