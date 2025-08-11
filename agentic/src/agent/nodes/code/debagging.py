"""..."""

from typing import override, Optional, List
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agent.prompts.code.debugging import code_debugging_prompt
from agent.models.anthropic_ import code_debagging_model
from agent.nodes.base import BaseNode
from agent.nodes.code.generation import dependencies
from services.memory import agent_memory_service


class CodeDebaggingNode(BaseNode):
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
        code: str,
        dataset_summary: str,
        error_message: str,
        dependencies: List[str] = dependencies,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
    ):
        """..."""
        print("Error to fix:", error_message)
        history = pickle.loads(
            self.memory.get_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ).code_context
        )
        persisted_variables = pickle.loads(
            self.memory.get_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ).persisted_variables
        )
        self._token_buffer = []
        persisted_variables = [key for key in persisted_variables.keys()]
        async for chunk in self._chain.astream(
            {
                "question": question,
                "code": code,
                "dependencies": dependencies,
                "error_message": error_message,
                "code_context": history,
                "dataset_summary": dataset_summary,
                "persisted_variables": persisted_variables
            }
        ):
            chunk = chunk.content
            self._token_buffer.append(chunk)
            yield chunk


code_debagging_node = CodeDebaggingNode(
    model=code_debagging_model,
    prompt=code_debugging_prompt,
    memory=agent_memory_service,
)
