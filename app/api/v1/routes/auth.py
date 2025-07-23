"""..."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth.service import AuthService
from app.services.user.service import UserService
from app.db.manager import db_manager
from app.schemas import user as user_schema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(
    user: user_schema.UserCreate, db: Session = Depends(db_manager.get_db)
):
    return UserService.create_user(db=db, user=user)


@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_manager.get_db),
):
    return AuthService.login(db=db, email=user.username, password=user.password)


@router.get("/me")
def get_current_user(
    token: str = Depends(AuthService.oauth2_scheme),
    db: Session = Depends(db_manager.get_db),
):
    return AuthService.get_current_user(db=db, token=token)
