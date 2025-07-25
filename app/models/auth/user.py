"""..."""

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    """..."""

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    datasets: Mapped[List["Dataset"]] = relationship("Dataset", back_populates="user")
