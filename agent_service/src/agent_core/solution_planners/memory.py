""" "..."""

from uuid import UUID
from typing import List, Any
import pickle


from pydantic import BaseModel, PrivateAttr, ConfigDict
from sqlalchemy.orm import Session
from langchain_core.messages import BaseMessage, HumanMessage
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables import Runnable

from agent_core.cache.chat_history import (
    ChatHistoryCacheManager,
    chat_history_cache_manager,
)
from agent_core.models.registry import anthropic_claude_sonnet_4_20250514_model


class SolutionsMemoryManager(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    chat_history_cache_manager: ChatHistoryCacheManager
    model: Runnable
    _summarization_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        summarization_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    """You are an expert data scientist tasked with summarizing previous assistant outputs.

Your job is to produce a very brief, factual summary that lists only the key design decisions, plans, or strategies explicitly described in the prior assistant messages.

Important:
- Do NOT include any information about actual implementation, code, or completed work.
- Do NOT add explanations, reasoning, or assumptions.
- Do NOT repeat information or add commentary.
- Only list design intents, planned steps, or decisions as explicitly stated.
- The summary should be concise and focused strictly on what was planned or designed to be done.

Format:
- Use a concise bullet-point or comma-separated list.
- Each item should describe a plan or decision, not a completed action.."""
                ),
                HumanMessage("{messages}"),
            ]
        )

        self._summarization_chain = summarization_prompt | self.model

    def get_solutions_history(self, db: Session, session_id: UUID) -> List[BaseMessage]:
        """..."""
        chat_history = self.chat_history_cache_manager.get_chat_history(
            db=db, session_id=session_id
        )
        solutions: List[BaseMessage] = pickle.loads(chat_history.solutions)
        return solutions

    def update_solutions_history(
        self,
        db: Session,
        session_id: UUID,
        question: str,
        new_solutions: List[str],
    ) -> None:
        """Update the solution message history with a new question and its summarized response."""
        summarized_messages = self.summarize_solutions(new_solutions)

        history = self.chat_history_cache_manager.get_chat_history(db, session_id)
        history_messages: List[BaseMessage] = pickle.loads(history.solutions)

        # Append new content
        history_messages.append(HumanMessage(content=question))
        history_messages.extend(summarized_messages)

        # Save updated messages
        history.solutions = pickle.dumps(history_messages)
        self.chat_history_cache_manager.cache_chat_history(session_id, history)

    def summarize_solutions(self, solutions: List[str]) -> List[BaseMessage]:
        """Generate a summary message from solution steps."""
        raw_text = "\n".join(solutions)
        summary: BaseMessage = self._summarization_chain.invoke({"messages": raw_text})
        return [summary]


solutions_memory_manager = SolutionsMemoryManager(
    chat_history_cache_manager=chat_history_cache_manager,
    model=anthropic_claude_sonnet_4_20250514_model,
)
