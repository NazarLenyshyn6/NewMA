"""..."""

from typing import Optional

from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.schemas import user as user_schemas
from app.repositories import user as user_repository
from app.services.auth.hashing import bcrypt_


class UserService:
    """..."""

    @staticmethod
    def get_user(db: Session, email: EmailStr) -> Optional[user_schemas.UserInDB]:
        """..."""
        db_user = user_repository.UserRepository.get_user(db=db, email=email)
        if not db_user:
            return None
        return user_schemas.UserInDB.model_validate(db_user)

    @staticmethod
    def create_user(
        db: Session, user: user_schemas.UserCreate
    ) -> user_schemas.UserRead:
        """..."""
        hashed_password = bcrypt_.bcrypt_hasher.hash(user.password)
        user_data = user.model_dump()
        user_data["password"] = hashed_password
        db_user = user_repository.UserRepository.create_user(db=db, user_data=user_data)
        return user_schemas.UserRead.model_validate(db_user)
