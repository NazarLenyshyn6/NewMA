"""..."""

from typing import override, Optional
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agent.prompts.responses.contextual import contextual_response_prompt
from agent.models.anthropic_ import contextual_response_model
from agent.nodes.base import BaseNode
from services.memory import agent_memory_service


class ContextualResponseNode(BaseNode):
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
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
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
        async for chunk in self._chain.astream(
            {"question": question, "history": history}
        ):
            chunk = chunk.content
            self._token_buffer.append(chunk)
            yield chunk


contextual_response_node = ContextualResponseNode(
    model=contextual_response_model,
    prompt=contextual_response_prompt,
    memory=agent_memory_service,
)
