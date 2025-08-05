"""..."""

from uuid import UUID
import pickle

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from services.chat_history import ChatHistoryService
from agent.summarizers.code.generator import GeneratedCodeSummarizer


class CodeGeneratorMemoryManager(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    chat_history_service: ChatHistoryService
    summarizer: GeneratedCodeSummarizer

    def get_code_history(
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
        code_history_bytes = chat_history.code
        code_history: str = pickle.loads(code_history_bytes)
        return code_history

    def update_code_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        new_code: str,
    ) -> None:
        code_history = self.get_code_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        new_code_history = self.summarizer.summarize(
            summary=code_history, generated_code=new_code
        )
        self.chat_history_service.update_chat_history_cache(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
            code_update=pickle.dumps(new_code_history),
        )
