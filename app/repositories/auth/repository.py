"""..."""

from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.models.auth.user import User


class AuthRepository:
    """..."""

    @staticmethod
    def get_user_by_id(db: Session, id: str) -> Optional[User]:
        """..."""
        return db.query(User).where(User.id == id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr) -> Optional[User]:
        """..."""
        return db.query(User).where(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        """..."""
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
