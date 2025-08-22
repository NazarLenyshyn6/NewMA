"""..."""

from typing import override, Optional
from uuid import UUID
import pickle
import json

from sqlalchemy.orm import Session

from agents.prompts.business.conversation import business_conversation_prompt
from agents.models.anthropic_ import business_conversation_model
from agents.nodes.base import BaseNode
from services.memory import agent_memory_service


class BusinessConversationNode(BaseNode):
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
            chunk = f"data: {json.dumps({'type': 'text', 'data': chunk})}\n\n"
            yield chunk


business_conversation_node = BusinessConversationNode(
    model=business_conversation_model,
    prompt=business_conversation_prompt,
    memory=agent_memory_service,
)
