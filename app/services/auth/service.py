"""..."""

from dataclasses import dataclass
from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.schemas.auth import token as token_schemas
from app.schemas.auth import user as user_schemas
from app.repositories.auth.repository import AuthRepository
from app.services.auth.jwt_handler import JWTHandler, jwt_handler
from app.services.auth.hashing.base import IHasher
from app.services.auth.hashing.bcrypt import bcrypt_hasher


@dataclass
class AuthService:
    jwt_handler: JWTHandler
    hasher: IHasher
    oauth2_scheme: OAuth2PasswordBearer

    @staticmethod
    def _get_user_by_id(db: Session, id: str) -> Optional[user_schemas.UserInDB]:
        """..."""
        db_user = AuthRepository.get_user_by_id(db=db, id=id)
        if not db_user:
            return None
        return user_schemas.UserInDB.model_validate(db_user)

    @staticmethod
    def _get_user_by_email(
        db: Session, email: EmailStr
    ) -> Optional[user_schemas.UserInDB]:
        """..."""
        db_user = AuthRepository.get_user_by_email(db=db, email=email)
        if not db_user:
            return None
        return user_schemas.UserInDB.model_validate(db_user)

    @staticmethod
    def _create_user(
        db: Session, user: user_schemas.UserCreate
    ) -> user_schemas.UserRead:
        """..."""
        hashed_password = bcrypt_hasher.hash(user.password)
        user_data = user.model_dump()
        user_data["password"] = hashed_password
        db_user = AuthRepository.create_user(db=db, user_data=user_data)
        return user_schemas.UserRead.model_validate(db_user)

    @classmethod
    def authenticate(
        cls, db: Session, email: EmailStr, password: str
    ) -> Optional[user_schemas.UserInDB]:
        """..."""
        user = cls._get_user_by_email(db=db, email=email)
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
        user = cls._get_user_by_id(db=db, id=token_data.id)
        if not user:
            raise cls.jwt_handler.credential_exception
        return user


auth_service = AuthService(
    jwt_handler=jwt_handler,
    hasher=bcrypt_hasher,
    oauth2_scheme=OAuth2PasswordBearer(tokenUrl="api/v1/auth/login"),
)
