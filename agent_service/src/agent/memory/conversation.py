"""..."""

from uuid import UUID
import pickle

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from services.chat_history import ChatHistoryService


class ConversationMemoryManager(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    chat_history_service: ChatHistoryService

    def get_conversation_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ) -> str:
        """..."""
        chat_history = self.chat_history_service.get_chat_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        conversation_history_bytes = chat_history.conversation
        conversation_history: str = pickle.loads(conversation_history_bytes)
        return conversation_history

    def update_conversation_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        new_conversation: str,
    ) -> None:
        """..."""
        self.chat_history_service.update_chat_history_cache(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
            conversation_update=pickle.dumps(new_conversation),
        )
