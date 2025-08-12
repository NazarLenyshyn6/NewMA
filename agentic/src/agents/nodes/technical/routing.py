from typing import override, Optional
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agents.prompts.technical.routing import routing_prompt
from agents.models.anthropic_ import routing_model
from agents.nodes.base import BaseNode
from services.memory import agent_memory_service



class RoutingNode(BaseNode):
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

routing_node = RoutingNode(model=routing_model, prompt=routing_prompt,memory=agent_memory_service,)