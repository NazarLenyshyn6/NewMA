"""..."""

import re
import pickle
from uuid import UUID
from typing import Optional, override, List

from sqlalchemy.orm import Session
from langchain_core.runnables import RunnableParallel, RunnableLambda

from agent.nodes.base import BaseParallelNode
from agent.prompts.summarization.code import code_summarization_prompt
from agent.prompts.summarization.conversation import conversation_summarization_prompt
from services.memory import agent_memory_service
from schemas.memory import AgentMemory
from agent.models.anthropic_ import summarization_model


class ParallelSummarizationNode(BaseParallelNode):
    """..."""

    @staticmethod
    def _extract_code(message: str) -> Optional[str]:
        """..."""
        pattern = r"```(?:python)?\n(.*?)(?:\n```)?$"
        match = re.search(pattern, message.strip(), re.DOTALL)

        if not match:
            return None

        return match.group(1).strip()

    @override
    def run(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        code_generation_message: str,
        conversation: str,
        question: str,
        persisted_variables: List,
    ):
        """..."""

        # Get data
        history: AgentMemory = self.memory.get_memory(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        code = self._extract_code(code_generation_message)

        # Create chains
        code_summarization_chain = (
            RunnableLambda(
                lambda input: {
                    "code": input["code"],
                    "history": input["code_history"],
                    "persisted_variables": f"{persisted_variables}",
                }
            )
            | code_summarization_prompt
            | self.model
        )

        conversation_summarization_chain = (
            RunnableLambda(
                lambda input: {
                    "conversation": input["conversation"],
                    "history": input["conversation_history"],
                    "question": question,
                }
            )
            | conversation_summarization_prompt
            | self.model
        )

        parallel_chain = RunnableParallel(
            {
                "code_memory": code_summarization_chain,
                "conversation_memory": conversation_summarization_chain,
            }
        )

        inputs = {
            "code": code,
            "code_history": pickle.loads(history.code_context),
            "conversation": conversation,
            "conversation_history": pickle.loads(history.conversation_context),
            "persisted_variables": persisted_variables,
            "question": question,
        }

        return parallel_chain.invoke(inputs)


parallel_summarization_node = ParallelSummarizationNode(
    model=summarization_model, memory=agent_memory_service
)
