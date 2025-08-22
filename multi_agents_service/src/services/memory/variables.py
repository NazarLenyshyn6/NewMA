"""..."""

from uuid import UUID
from typing import override
import pickle

from sqlalchemy.orm import Session

from services.memory.base import BaseMemoryService
from schemas.memory import VariablesMemory
from cache.memory import variables_memory_cache
from repositories.memory import variables_memory_repository
from loaders.local import LocalLoader


class VariablesMemoryService(BaseMemoryService[VariablesMemory]):
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
        df = self.loader.load(storage_uri=storage_uri)

        memory_schema = VariablesMemory(
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            memory=pickle.dumps({"df": df}),
        )
        self.memory_repository.create_memory(db=db, memory_schema=memory_schema)

        # Cache the newly created chat history to speed up future accesses
        self.memory_cache.cache_memory(
            session_id=session_id, file_name=file_name, memory_schema=memory_schema
        )

        return memory_schema


variables_memory_service = VariablesMemoryService(
    memory_cache=variables_memory_cache,
    memory_repository=variables_memory_repository,
    memory_schema=VariablesMemory,
    loader=LocalLoader,
)
