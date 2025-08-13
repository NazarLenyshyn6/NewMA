"""..."""

from typing import override, Optional
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agents.prompts.summarization.conversation.technical import technical_conversation_summarization_prompt

from agents.models.anthropic_ import summarization_model
from agents.nodes.base import BaseNode
from services.memory import agent_memory_service


class TechicalConversationSummarizationNode(BaseNode):
    """..."""

    @override
    def run(
        self,
        question: str,
        conversation: str,
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
            ).conversation_context
        )
        return self._chain.invoke(
            {"conversation": conversation, "history": history, "question": question}
        ).content

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


technical_conversation_summarization_node = TechicalConversationSummarizationNode(
    model=summarization_model,
    prompt=technical_conversation_summarization_prompt,
    memory=agent_memory_service,
)
