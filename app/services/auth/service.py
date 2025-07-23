"""..."""

from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.services.user.service import UserService
from app.services.auth.jwt_ import JWTHandler, jwt_handler
from app.services.auth.hashing.base import IHasher
from app.services.auth.hashing.bcrypt_ import bcrypt_hasher
from app.schemas import user as user_schemas
from app.schemas import token as token_schemas


class AuthService:
    jwt_handler: JWTHandler = jwt_handler
    hasher: IHasher = bcrypt_hasher
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

    @classmethod
    def authenticate(
        cls, db: Session, email: EmailStr, password: str
    ) -> Optional[user_schemas.UserInDB]:
        """..."""
        user = UserService.get_user_by_email(db=db, email=email)
        if not user or not cls.hasher.verify(password, user.password):
            return None
        return user

    @classmethod
    def login(cls, db: Session, email: str, password: str) -> token_schemas.Token:
        """..."""
        user = cls.authenticate(db=db, email=email, password=password)
        if not user:
            raise cls.jwt_handler.credential_exception
        access_token = cls.jwt_handler.create_access_token(data={"sub": str(user.id)})
        return token_schemas.Token(access_token=access_token, token_type="bearer")

    @classmethod
    def get_current_user(cls, db: Session, token: str) -> user_schemas.UserInDB:
        """..."""
        token_data = cls.jwt_handler.decode_access_token(token=token)
        user = UserService.get_user_by_id(db=db, id=token_data.id)
        if not user:
            raise cls.jwt_handler.credential_exception
        return user
