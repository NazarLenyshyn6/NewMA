"""..."""

from uuid import UUID
from typing import Optional, TypeVar, Generic, Any
from dataclasses import dataclass

from sqlalchemy.orm import Session


from schemas.memory import BaseMemory as BaseMemorySchema
from models.memory import BaseMemory as BaseMemoryModel
from models.memory import (
    ConversationSummaryMemory,
    ConversationMemory,
    CodeSummaryMemory,
    VariablesMemory,
)

S = TypeVar("S", bound=BaseMemorySchema)
M = TypeVar("M", bound=BaseMemoryModel)


@dataclass
class BaseMemoryRepository(Generic[S, M]):
    memory_model: type[M]

    def create_memory(self, db: Session, memory_schema: S) -> M:
        """..."""
        db_memory = self.memory_model(**memory_schema.model_dump())
        db.add(db_memory)
        db.commit()
        db.refresh(db_memory)
        return db_memory

    def get_memory(
        self, db: Session, user_id: int, session_id: UUID, file_name: str
    ) -> Optional[M]:
        """..."""
        return (
            db.query(self.memory_model)
            .filter_by(user_id=user_id, session_id=session_id, file_name=file_name)
            .first()
        )

    def update_memory(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        memory_schema: S,
    ) -> None:
        """..."""
        memory_history = self.get_memory(
            db=db, user_id=user_id, session_id=session_id, file_name=file_name
        )

        update_data = memory_schema.model_dump(exclude_none=True)

        for field, value in update_data.items():
            setattr(memory_history, field, value)

        db.commit()
        db.refresh(memory_history)
        return memory_history

    def delete_memory(self, db: Session, user_id: int, file_name: str) -> None:
        """..."""
        db.query(self.memory_model).filter(
            self.memory_model.user_id == user_id,
            self.memory_model.file_name == file_name,
        ).delete(synchronize_session=False)

        db.commit()


conversation_summary_memory_repository = BaseMemoryRepository(
    memory_model=ConversationSummaryMemory
)
conversation_memory_repository = BaseMemoryRepository(memory_model=ConversationMemory)
code_summary_memory_repository = BaseMemoryRepository(memory_model=CodeSummaryMemory)
variables_memory_repository = BaseMemoryRepository(memory_model=VariablesMemory)
