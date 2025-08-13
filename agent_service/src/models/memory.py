"""..."""

from uuid import UUID

from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from models.base import Base


class AgentMemory(Base):
    """..."""

    __tablename__ = "agent_memory"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    file_name: Mapped[str] = mapped_column(primary_key=True)

    conversation_context: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    conversation_history: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    code_context: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    persisted_variables: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
