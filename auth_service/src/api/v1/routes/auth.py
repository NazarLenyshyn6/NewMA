"""..."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from core.db import db_manager
from schemas.user import UserCreate
from services.user import UserService
from services.auth import auth_service_

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(db_manager.get_db),
):
    return auth_service_.get_current_user(db=db, token=token)


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(db_manager.get_db)):
    return UserService.create_user(db=db, user=user)


@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_manager.get_db),
):
    return auth_service_.login(db=db, email=user.username, password=user.password)
