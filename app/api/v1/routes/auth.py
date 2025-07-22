"""..."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth.service import AuthService
from app.db.manager import db_manager

router = APIRouter(prefix="/login", tags=["Auth"])


@router.post("/")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_manager.get_db),
):
    return AuthService.login(db=db, email=user.username, password=user.password)
