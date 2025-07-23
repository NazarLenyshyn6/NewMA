"""..."""

from typing import Optional

from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.models import user as user_models


class UserRepository:
    """..."""

    @staticmethod
    def get_user_by_id(db: Session, id: str) -> Optional[user_models.User]:
        """..."""
        return db.query(user_models.User).where(user_models.User.id == id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr) -> Optional[user_models.User]:
        """..."""
        return db.query(user_models.User).where(user_models.User.email == email).first()

    @staticmethod
    def create_user(db: Session, user_data: dict) -> user_models.User:
        """..."""
        db_user = user_models.User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
