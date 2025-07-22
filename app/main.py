"""..."""

import uvicorn
from fastapi import FastAPI

from app.models import user
from app.db.manager import db_manager
from app.api.v1.router import api_router


user.Base.metadata.create_all(bind=db_manager.engine)


app = FastAPI()


app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
