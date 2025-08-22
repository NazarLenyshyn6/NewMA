"""..."""

from uuid import UUID
from typing import override
import pickle

from sqlalchemy.orm import Session

from services.memory.base import BaseMemoryService
from schemas.memory import ConversationMemory
from cache.memory import conversation_memory_cache
from repositories.memory import conversation_memory_repository


class ConversationMemoryService(BaseMemoryService[ConversationMemory]):
    """..."""

    @override
    def create_memory(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ):
        """..."""
        memory_schema = ConversationMemory(
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            memory=pickle.dumps([]),
        )
        self.memory_repository.create_memory(db=db, memory_schema=memory_schema)

        # Cache the newly created chat history to speed up future accesses
        self.memory_cache.cache_memory(
            session_id=session_id, file_name=file_name, memory_schema=memory_schema
        )

        return memory_schema


conversation_memory_service = ConversationMemoryService(
    memory_cache=conversation_memory_cache,
    memory_repository=conversation_memory_repository,
    memory_schema=ConversationMemory,
)
