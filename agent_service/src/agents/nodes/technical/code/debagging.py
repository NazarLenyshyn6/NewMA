"""..."""

from typing import override, Optional, List
from uuid import UUID
import pickle
import json

from pydantic import PrivateAttr
from sqlalchemy.orm import Session

from agents.prompts.technical.code.debagging import code_debugging_prompt
from agents.models.anthropic_ import code_generation_model
from agents.nodes.base import BaseNode
from agents.nodes.technical.code.generation import dependencies
from services.memory import agent_memory_service


class CodeDebaggingNode(BaseNode):
    """..."""

    _token_buffer_text: list = PrivateAttr(default_factory=list)

    def get_steamed_tokens_text(self) -> str:
        return "".join(self._token_buffer_text)

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
                "persisted_variables": persisted_variables,
            }
        ):
            chunk = chunk.content
            self._token_buffer_text.append(chunk)
            self._token_buffer.append(chunk)
            chunk = f"data: {json.dumps({'type': 'text', 'data': chunk})}\n\n"
            yield chunk


code_debagging_node = CodeDebaggingNode(
    model=code_generation_model,
    prompt=code_debugging_prompt,
    memory=agent_memory_service,
)
