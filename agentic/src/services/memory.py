"""..."""

from typing import Optional
from uuid import UUID
from dataclasses import dataclass
import pickle

from sqlalchemy.orm import Session

from loaders.local import LocalLoader
from repositories.memory import AgentMemoryRepository
from cache.memory import AgentMemoryCacheManager, agent_memory_cache_manager
from schemas.memory import AgentMemory


@dataclass
class AgentMemoryService:
    """..."""

    agent_memory_cache_manager: AgentMemoryCacheManager

    def get_memory(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ) -> AgentMemory:
        """..."""
        # Attempt to retrieve chat history from cache for faster access
        cached_memory = self.agent_memory_cache_manager.get_memory(
            session_id=session_id, file_name=file_name
        )
        if cached_memory is not None:
            return cached_memory

        # Cache miss: fetch chat history from the database
        db_memory = AgentMemoryRepository.get_memory(
            db=db, user_id=user_id, session_id=session_id, file_name=file_name
        )
        if db_memory is not None:
            memory_schema = AgentMemory.model_validate(db_memory)

            # Cache the retrieved chat history for future quick access
            self.agent_memory_cache_manager.cache_memory(
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

    def get_conversation_memory(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ):
        """..."""
        memory = self.get_memory(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        return pickle.loads(memory.conversation_history)

    def create_memory(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ) -> AgentMemory:
        """..."""
        # Load base data from the specified local storage pat (Will be replaced with cloud storage)
        df = LocalLoader.load(storage_uri=storage_uri)

        # Create AgentMemory entity with initial empty pickled data for solutions and code,
        # and store the loaded DataFrame in variables after pickling

        memory_schema = AgentMemory(
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            conversation_context=pickle.dumps(""),
            conversation_history=pickle.dumps([]),
            code_context=pickle.dumps(""),
            persisted_variables=pickle.dumps({"df": df}),
        )

        # Persist the new chat history record into the database
        AgentMemoryRepository.create_memory(db=db, memory_schema=memory_schema)

        # Cache the newly created chat history to speed up future accesses
        self.agent_memory_cache_manager.cache_memory(
            session_id=session_id, file_name=file_name, memory_schema=memory_schema
        )

        return memory_schema

    def update_memory_cache(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        conversation_context: Optional[bytes] = None,
        conversation_history: Optional[bytes] = None,
        persisted_variables: Optional[bytes] = None,
        code_context: Optional[bytes] = None,
    ):
        """..."""

        # Get current chat history
        memory_history = self.get_memory(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )

        # Update chat history
        updatable_variables = [
            "conversation_context",
            "conversation_history",
            "code_context",
            "persisted_variables",
        ]
        for field in updatable_variables:
            new_value = getattr(memory_history, field, None)
            if new_value is not None:
                setattr(memory_history, field, new_value)

        # Cache updated chat history
        self.agent_memory_cache_manager.cache_memory(
            session_id=session_id, file_name=file_name, memory_schema=memory_history
        )

    def save_memory(
        self, db: Session, user_id: int, session_id: UUID, file_name: str
    ) -> None:
        """..."""

        # Get chat history from cache
        cached_memory: AgentMemory = self.agent_memory_cache_manager.get_memory(
            session_id=session_id, file_name=file_name
        )

        if cached_memory:
            AgentMemoryRepository.update_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                memory_schema=cached_memory,
            )

    def delete_memory(self, db: Session, user_id: int, file_name: str) -> None:
        """..."""
        AgentMemoryRepository.delete_memory(db=db, user_id=user_id, file_name=file_name)

        # Delete from cache (TODO)


agent_memory_service = AgentMemoryService(agent_memory_cache_manager)
