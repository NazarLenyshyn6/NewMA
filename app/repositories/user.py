"""..."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import user as user_models


class UserRepository:
    """..."""

    @staticmethod
    def get_users(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[user_models.User]:
        """..."""
        return db.query(user_models.User).offset(skip).limit(limit).all()

    @staticmethod
    def get_user(db: Session, id: int) -> Optional[user_models.User]:
        """..."""
        return db.query(user_models.User).where(user_models.User.id == id).first()

    @staticmethod
    def create_user(db: Session, user_data: dict) -> user_models.User:
        """..."""
        db_user = user_models.User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
