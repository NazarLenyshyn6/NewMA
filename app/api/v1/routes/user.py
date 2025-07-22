"""..."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.manager import db_manager
from app.services.user.service import UserService
from app.schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(user: user_schema.UserCreate, db: Session = Depends(db_manager.get_db)):
    return UserService.create_user(db=db, user=user)
