"""..."""

from uuid import UUID
from typing import Optional

from sqlalchemy.orm import Session

from schemas.memory import AgentMemory as AgentMemorySchema
from models.memory import AgentMemory as AgentMemoryModel


class AgentMemoryRepository:
    """..."""

    @classmethod
    def create_memory(
        cls, db: Session, memory_schema: AgentMemorySchema
    ) -> AgentMemoryModel:
        """..."""
        db_memory = AgentMemoryModel(**memory_schema.model_dump())
        db.add(db_memory)
        db.commit()
        db.refresh(db_memory)
        return db_memory

    @classmethod
    def get_memory(
        cls, db: Session, user_id: int, session_id: UUID, file_name: str
    ) -> Optional[AgentMemoryModel]:
        """..."""
        return (
            db.query(AgentMemoryModel)
            .filter_by(user_id=user_id, session_id=session_id, file_name=file_name)
            .first()
        )

    @classmethod
    def update_memory(
        cls,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        memory_schema: AgentMemorySchema,
    ) -> None:
        """..."""
        memory_history = cls.get_memory(
            db=db, user_id=user_id, session_id=session_id, file_name=file_name
        )

        if memory_schema.conversation_history is not None:
            print("Conversation history")
            memory_history.conversation_history = memory_schema.conversation_history

        if memory_schema.conversation_context is not None:
            print("Conversation context")
            memory_history.conversation_context = memory_schema.conversation_context

        if memory_schema.code_context is not None:
            print("Code context")
            memory_history.code_context = memory_schema.code_context

        if memory_schema.conversation_context is not None:
            print("Variables")
            memory_history.persisted_variables = memory_schema.persisted_variables

        db.commit()

    @classmethod
    def delete_memory(cls, db: Session, user_id: int, file_name: str) -> None:
        """..."""
        db.query(AgentMemoryModel).filter(
            AgentMemoryModel.user_id == user_id, AgentMemoryModel.file_name == file_name
        ).delete(synchronize_session=False)

        db.commit()
