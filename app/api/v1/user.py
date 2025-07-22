"""..."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.manager import db_manager
from app.services.user.service import UserService
from app.schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(db_manager.get_db)
):
    return UserService.get_users(db=db, skip=skip, limit=limit)


@router.post("/")
def create_user(user: user_schema.UserCreate, db: Session = Depends(db_manager.get_db)):
    return UserService.create_user(db=db, user=user)
