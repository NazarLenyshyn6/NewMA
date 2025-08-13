"""..."""

from typing import override, Optional
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agents.prompts.technical.planning import planning_prompt
from agents.models.anthropic_ import planning_model
from agents.nodes.base import BaseNode
from services.memory import agent_memory_service


class PlanningNode(BaseNode):
    """..."""

    @override
    def run(
        self,
        question: str,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
    ): ...

    @override
    async def arun(
        self,
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ):
        """..."""
        self._token_buffer = []
        history = pickle.loads(
            self.memory.get_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ).conversation_context
        )
        print("Conversation history:", history)
        async for chunk in self._chain.astream(
            {"question": question, "history": history}
        ):
            chunk = chunk.content
            self._token_buffer.append(chunk)
            yield chunk


planning_node = PlanningNode(
    model=planning_model,
    prompt=planning_prompt,
    memory=agent_memory_service,
)
