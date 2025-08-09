"""..."""

from typing import override, Optional
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agent.prompts.summarization.conversation import conversation_summarization_prompt
from agent.models.anthropic_ import summarization_model
from agent.nodes.base import BaseNode
from services.memory import agent_memory_service


class ConversationSummarizationNode(BaseNode):
    """..."""

    @override
    def run(
        self,
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
            ).code_context
        )
        return self._chain.invoke(
            {"conversation": conversation, "history": history}
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


conversation_summarization_node = ConversationSummarizationNode(
    model=summarization_model,
    prompt=conversation_summarization_prompt,
    memory=agent_memory_service,
)
