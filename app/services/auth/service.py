"""..."""

from dataclasses import dataclass
from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.core.logger_setup import configure_logger
from app.schemas.auth import token as token_schemas
from app.schemas.auth import user as user_schemas
from app.repositories.auth.repository import AuthRepository
from app.services.auth.jwt_handler import JWTHandler, jwt_handler
from app.services.auth.hashing.base import IHasher
from app.services.auth.hashing.bcrypt import bcrypt_hasher

logger = configure_logger(
    name="service_auth", subfolder="services", filename="auth.log"
)


@dataclass
class AuthService:
    jwt_handler: JWTHandler
    hasher: IHasher
    oauth2_scheme: OAuth2PasswordBearer

    @staticmethod
    def _get_user_by_id(db: Session, id: str) -> Optional[user_schemas.UserInDB]:
        """..."""
        logger.debug("Fetching user by ID: %s", id)
        db_user = AuthRepository.get_user_by_id(db=db, id=id)
        if not db_user:
            logger.warning("User not found by ID: %s", id)
            return None
        return user_schemas.UserInDB.model_validate(db_user)

    @staticmethod
    def _get_user_by_email(
        db: Session, email: EmailStr
    ) -> Optional[user_schemas.UserInDB]:
        """..."""
        logger.debug("Fetching user by email: %s", email)
        db_user = AuthRepository.get_user_by_email(db=db, email=email)
        if not db_user:
            logger.warning("User not found by email: %s", email)
            return None
        return user_schemas.UserInDB.model_validate(db_user)

    @staticmethod
    def _create_user(
        db: Session, user: user_schemas.UserCreate
    ) -> user_schemas.UserRead:
        """..."""
        logger.info("Creating user with email: %s", user.email)
        try:
            hashed_password = bcrypt_hasher.hash(user.password)
            user_data = user.model_dump()
            user_data["password"] = hashed_password
            db_user = AuthRepository.create_user(db=db, user_data=user_data)
            return user_schemas.UserRead.model_validate(db_user)
        except Exception:
            logger.exception("Failed to create user with email: %s", user.email)
            raise

    def authenticate(
        self, db: Session, email: EmailStr, password: str
    ) -> Optional[user_schemas.UserInDB]:
        """..."""
        logger.debug("Authenticating user by email: %s", email)
        user = self._get_user_by_email(db=db, email=email)
        if not user or not self.hasher.verify(password, user.password):
            logger.warning("Authentication failed: user not found by email: %s", email)
            return None
        return user

    def login(self, db: Session, email: str, password: str) -> token_schemas.Token:
        """..."""
        logger.info("Login attempt for email: %s", email)
        user = self.authenticate(db=db, email=email, password=password)
        if not user:
            logger.warning("Login failed for email: %s", email)
            raise self.jwt_handler.credential_exception
        access_token = self.jwt_handler.create_access_token(data={"sub": str(user.id)})
        logger.info("Login successful, token created for user id: %s", user.id)
        return token_schemas.Token(access_token=access_token, token_type="bearer")

    def get_current_user(self, db: Session, token: str) -> user_schemas.UserInDB:
        """..."""
        logger.debug("Getting current user from token")
        token_data = self.jwt_handler.decode_access_token(token=token)
        user = self._get_user_by_id(db=db, id=token_data.id)
        if not user:
            logger.warning("Current user not found for token")
            raise self.jwt_handler.credential_exception
        logger.debug("Current user retrieved user_id=%s", user.id)
        return user


auth_service = AuthService(
    jwt_handler=jwt_handler,
    hasher=bcrypt_hasher,
    oauth2_scheme=OAuth2PasswordBearer(tokenUrl="api/v1/auth/login"),
)
