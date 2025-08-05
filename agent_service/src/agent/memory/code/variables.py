"""..."""

from uuid import UUID
import pickle

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from services.chat_history import ChatHistoryService


class CodeVariablesMemoryManager(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    chat_history_service: ChatHistoryService

    def get_code_variables_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ) -> dict:
        """..."""
        chat_history = self.chat_history_service.get_chat_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        code_variables_history_bytes = chat_history.variables
        code_history: dict = pickle.loads(code_variables_history_bytes)
        return code_history

    def update_code_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        new_code_variables: dict,
    ) -> None:
        self.chat_history_service.update_chat_history_cache(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
            variables_update=pickle.dumps(new_code_variables),
        )
