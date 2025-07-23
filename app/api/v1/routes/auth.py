"""..."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from app.db.manager import db_manager
from app.schemas.auth import user as user_schema
from app.services.auth.service import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(
    user: user_schema.UserCreate, db: Session = Depends(db_manager.get_db)
):
    return auth_service._create_user(db=db, user=user)


@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_manager.get_db),
):
    return auth_service.login(db=db, email=user.username, password=user.password)


@router.get("/me")
def get_current_user(
    token: str = Depends(auth_service.oauth2_scheme),
    db: Session = Depends(db_manager.get_db),
):
    return auth_service.get_current_user(db=db, token=token)
