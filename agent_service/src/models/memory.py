"""
Agent memory database model.

This module defines the `Memory` ORM model, which represents
persistent storage of user sessions and their associated memory artifacts.
It stores binary-encoded summaries (analysis, visualization, code, variables,
and conversation) tied to a specific user, session, and file.

The model ensures each memory record is uniquely identified by a composite
primary key (`user_id`, `session_id`, `file_name`).

Classes:
    Memory: ORM model for storing per-session agent memory,
                 including summaries and conversations.
"""

from uuid import UUID

from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from models.base import Base


class Memory(Base):
    """
    ORM model for storing per-session agent memory.

    This model captures all serialized memory components of an agent’s
    interaction with a user, including analysis results, visualizations,
    code summaries, variable snapshots, and full conversation history.
    It is uniquely identified by the combination of `user_id`,
    `session_id`, and `file_name`.

    Attributes:
        user_id: Identifier for the user associated with the memory.
        session_id: Unique session identifier, stored as a PostgreSQL UUID.
        file_name: The name of the file or context the memory belongs to.
        analysis_summary: Binary-encoded summary of analysis results.
        visualization_summary: Binary-encoded summary of visualization results.
        code_summary: Binary-encoded summary of code-related insights.
        variables: Binary-encoded snapshot of variables used in the session.
        conversation: Binary-encoded representation of the full conversation.
    """

    __tablename__ = "agent_memory"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    file_name: Mapped[str] = mapped_column(primary_key=True)

    analysis_summary: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    visualization_summary: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    code_summary: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    user_preferences_summary: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    variables: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    conversation: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
