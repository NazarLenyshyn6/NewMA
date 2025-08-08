"""..."""

from typing import override, Optional
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agent.prompts.desicion import desicion_prompt
from agent.models.anthropic_ import desicion_model
from agent.nodes.base import BaseNode
from services.memory import agent_memory_service


class DecisionNode(BaseNode):
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
    ):
        history = pickle.loads(
            self.memory.get_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ).conversation_history
        )
        return self._chain.invoke({"question": question, "history": history}).content

    @override
    def arun(
        self,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
        *args,
        **kwargs
    ): ...


decision_node = DecisionNode(
    model=desicion_model,
    prompt=desicion_prompt,
    memory=agent_memory_service,
)
