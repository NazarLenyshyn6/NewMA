"""..."""

from uuid import UUID

from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from models.base import Base


class ChatHistory(Base):
    """..."""

    __tablename__ = "chat_histories"

    session_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    solutions: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    code: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    variables: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
