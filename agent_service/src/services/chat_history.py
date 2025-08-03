"""..."""

from uuid import UUID
from dataclasses import dataclass
import pickle

from sqlalchemy.orm import Session

from schemas.chat_history import ChatHistory
from loaders.local import LocalLoader
from repositories.chat_history import ChatHistoryRepository
from cache.chat_history import ChatHistoryCacheManager, chat_history_cache


@dataclass
class ChatHistoryService:
    """..."""

    chat_history_cache: ChatHistoryCacheManager

    def get_chat_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ) -> ChatHistory:
        """..."""

        # Attempt to retrieve chat history from cache for faster access
        cached_chat_history = self.chat_history_cache.get_chat_history(
            session_id=session_id, file_name=file_name
        )
        if cached_chat_history is not None:
            return cached_chat_history

        # Cache miss: fetch chat history from the database
        db_chat_history = ChatHistoryRepository.get_chat_history(
            db=db, user_id=user_id, session_id=session_id, file_name=file_name
        )
        if db_chat_history is not None:
            # Validate and parse DB model to Pydantic ChatHistory
            chat_history = ChatHistory.model_validate(db_chat_history)

            # Cache the retrieved chat history for future quick access
            self.chat_history_cache.cache_chat_history(
                session_id=session_id, file_name=file_name, chat_history=chat_history
            )
            return chat_history

        # Chat history not found in cache or DB: create a new chat history instance
        return self.create_chat_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            storage_uri=storage_uri,
            file_name=file_name,
        )

    def create_chat_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ) -> ChatHistory:
        """..."""

        # Load base data from the specified local storage pat (Will be replaced with cloud storage)
        df = LocalLoader.load(storage_uri=storage_uri)

        # Create ChatHistory entity with initial empty pickled data for solutions and code,
        # and store the loaded DataFrame in variables after pickling
        chat_history = ChatHistory(
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            solutions=pickle.dumps([]),
            code=pickle.dumps([]),
            variables=pickle.dumps({"df": df}),
        )

        # Persist the new chat history record into the database
        ChatHistoryRepository.create_chat_history(db=db, chat_history=chat_history)

        # Cache the newly created chat history to speed up future accesses
        self.chat_history_cache.cache_chat_history(
            session_id=session_id, file_name=file_name, chat_history=chat_history
        )

        return chat_history

    def update_chat_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        chat_history_update: ChatHistory,
    ) -> None:
        """..."""

        # Apply updates to the chat history record in the database
        ChatHistoryRepository.update_chat_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            chat_history_update=chat_history_update,
        )

        # Retrieve the updated chat history record from the database
        db_chat_history = ChatHistoryRepository.get_chat_history(
            db=db, user_id=user_id, session_id=session_id, file_name=file_name
        )
        chat_history = ChatHistory.model_validate(db_chat_history)

        # Update the cached chat history to reflect recent changes
        self.chat_history_cache.cache_chat_history(
            session_id=session_id, file_name=file_name, chat_history=chat_history
        )

    def delete_chat_history(self, db: Session, user_id: int, file_name: str) -> None:
        """..."""

        # Remove chat history entry from the database
        ChatHistoryRepository.delete_chat_history(
            db=db, user_id=user_id, file_name=file_name
        )

        # Delete from cache


chat_history_service = ChatHistoryService(chat_history_cache)
