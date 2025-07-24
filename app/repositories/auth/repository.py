"""..."""

from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.logger_setup import configure_logger
from app.models.auth.user import User

logger = configure_logger(
    name="repository_auth", subfolder="repositories", filename="auth.log"
)


class AuthRepository:
    """..."""

    @staticmethod
    def get_user_by_id(db: Session, id: str) -> Optional[User]:
        """..."""
        logger.debug("Fetching user by ID: %s", id)
        user = db.query(User).where(User.id == id).first()
        if not user:
            logger.warning("User not found by ID: %s", id)
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: EmailStr) -> Optional[User]:
        """..."""
        logger.debug("Fetching user by email: %s", email)
        user = db.query(User).where(User.email == email).first()
        if not user:
            logger.warning("User not found by email: %s", email)
        return user

    @staticmethod
    def create_user(db: Session, user_data: dict) -> User:
        """..."""
        logger.info("Creating new user with email: %s", user_data.get("email"))
        try:
            db_user = User(**user_data)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info("User created successfully with ID: %s", db_user.id)
            return db_user
        except Exception:
            logger.exception(
                "Failed to create user with email: %s", user_data.get("email")
            )
            db.rollback()
            raise
