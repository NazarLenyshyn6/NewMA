"""..."""

from uuid import UUID
import pickle

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from services.chat_history import ChatHistoryService
from agent.summarizers.planners import SolutionPlansSummarizer


class SolutionPlannerMemoryManager(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    chat_history_service: ChatHistoryService
    summarizer: SolutionPlansSummarizer

    def get_solutions_history(
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
        solutions_history_bytes = chat_history.solutions
        solutions_history: str = pickle.loads(solutions_history_bytes)
        return solutions_history

    def update_solutions_history(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        new_solutions: str,
    ) -> None:
        """..."""
        solutions_summary = self.get_solutions_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        new_solutions_summary = self.summarizer.summarize(
            solutions_summary, new_solutions
        )
        self.chat_history_service.update_chat_history_cache(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
            solutions_update=pickle.dumps(new_solutions_summary),
        )
