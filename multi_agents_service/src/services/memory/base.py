"""..."""

from typing import TypeVar, Generic, Any, Optional
from uuid import UUID
from dataclasses import dataclass
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from repositories.memory import BaseMemoryRepository
from cache.memory import BaseMemoryCache
from schemas.memory import BaseMemory as BaseMemorySchema
from loaders.base import BaseLoader

S = TypeVar("S", bound=BaseMemorySchema)


@dataclass
class BaseMemoryService(ABC, Generic[S]):
    """..."""

    memory_cache: BaseMemoryCache
    memory_repository: BaseMemoryRepository
    memory_schema: type[S]
    loader: Optional[type[BaseLoader]] = None

    def get_memory(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ) -> S:
        """..."""
        # Attempt to retrieve chat history from cache for faster access
        cached_memory = self.memory_cache.get_memory(
            session_id=session_id, file_name=file_name
        )
        if cached_memory is not None:
            return cached_memory

        # Cache miss: fetch chat history from the database
        db_memory = self.memory_repository.get_memory(
            db=db, user_id=user_id, session_id=session_id, file_name=file_name
        )
        if db_memory is not None:
            memory_schema = self.memory_schema.model_validate(db_memory)

            # Cache the retrieved chat history for future quick access
            self.memory_cache.cache_memory(
                session_id=session_id, file_name=file_name, memory_schema=memory_schema
            )
            return memory_schema

        # Chat history not found in cache or DB: create a new chat history instance
        return self.create_memory(
            db=db,
            user_id=user_id,
            session_id=session_id,
            storage_uri=storage_uri,
            file_name=file_name,
        )

    @abstractmethod
    def create_memory(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ) -> S:
        """..."""
        ...

    def update_memory_cache(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        update_value: Any,
    ) -> None:
        """..."""
        memory_history = self.get_memory(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )

        if update_value is not None:
            memory_history.memory = update_value

        # Cache updated chat history
        self.memory_cache.cache_memory(
            session_id=session_id, file_name=file_name, memory_schema=memory_history
        )

    def save_memory(
        self, db: Session, user_id: int, session_id: UUID, file_name: str
    ) -> None:
        """..."""

        # Get chat history from cache
        cached_memory: S = self.memory_cache.get_memory(
            session_id=session_id, file_name=file_name
        )

        if cached_memory is not None:
            self.memory_repository.update_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                memory_schema=cached_memory,
            )

    def delete_memory(self, db: Session, user_id: int, file_name: str) -> None:
        """..."""
        self.memory_repository.delete_memory(
            db=db, user_id=user_id, file_name=file_name
        )
