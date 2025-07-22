"""..."""

from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas import user as user_schemas
from app.repositories import user as user_repository
from app.services.auth.hashing import bcrypt_


class UserService:
    """..."""

    @staticmethod
    def get_users(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[user_schemas.UserRead]:
        """..."""
        db_users = user_repository.UserRepository.get_users(
            db=db, skip=skip, limit=limit
        )
        return [user_schemas.UserRead.model_validate(db_user) for db_user in db_users]

    @staticmethod
    def get_user(db: Session, id: int) -> user_schemas.UserRead:
        """..."""
        db_user = user_repository.UserRepository.get_user(db=db, id=id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} not dound",
            )
        return user_schemas.UserRead.model_validate(db_user)

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
