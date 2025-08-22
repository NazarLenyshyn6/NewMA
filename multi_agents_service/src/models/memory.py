"""..."""

from uuid import UUID

from datetime import datetime

from sqlalchemy import LargeBinary
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class BaseMemory(DeclarativeBase):
    """..."""

    __abstract__ = True

    user_id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    file_name: Mapped[str] = mapped_column(primary_key=True)
    memory: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class ConversationSummaryMemory(BaseMemory):
    """..."""

    __tablename__ = "conversation_summary_memory"


class ConversationMemory(BaseMemory):
    """..."""

    __tablename__ = "conversation_memory"


class CodeSummaryMemory(BaseMemory):
    """..."""

    __tablename__ = "code_summary_memory"


class VariablesMemory(BaseMemory):
    """..."""

    __tablename__ = "variables_memory"
