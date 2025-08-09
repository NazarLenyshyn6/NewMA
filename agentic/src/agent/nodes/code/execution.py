"""..."""

import re
from typing import override, Optional, List
from types import ModuleType
import importlib
from uuid import UUID
import pickle


from pydantic import PrivateAttr
from sqlalchemy.orm import Session

from agent.nodes.base import BaseNode
from services.memory import agent_memory_service
from agent.nodes.code.generation import dependencies
from agent.nodes.code.debagging import code_debagging_node, CodeDebaggingNode


class CodeExecutionNode(BaseNode):
    """..."""

    _debagged_token_buffer: list = PrivateAttr()

    @staticmethod
    def _import_dependencies(dependencies: List[str]):
        """..."""
        imported_modules = {}
        for package_name in dependencies:
            try:
                module = importlib.import_module(package_name)
                imported_modules[package_name] = module
            except Exception:
                ...
        return imported_modules

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
        code_generation_message: str,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
        dependencies: List[str] = dependencies,
        code_debagging_node: CodeDebaggingNode = code_debagging_node,
        current_attempt: int = 1,
        max_attempts: int = 5,
    ):
        """..."""
        if current_attempt > max_attempts:
            code_debagging_node._token_buffer = []
            yield "Failed"

        persisted_variables_history = pickle.loads(
            self.memory.get_memory(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ).persisted_variables
        )
        code = self._extract_code(code_generation_message)
        global_context = self._import_dependencies(dependencies)
        local_context = persisted_variables_history.copy()
        global_context.update(local_context)
        try:
            exec(code, global_context)
            local_context = {
                k: v
                for k, v in global_context.items()
                if k not in dependencies and not isinstance(v, ModuleType)
            }
            self._token_buffer += code_debagging_node._token_buffer
            self._debagged_token_buffer = code_debagging_node._token_buffer
            code_debagging_node._token_buffer = []
            yield local_context

        except Exception as e:
            async for chunk in code_debagging_node.arun(
                question=question,
                code=code,
                error_message=str(e),
                dependencies=dependencies,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            ):
                yield chunk
            fixed_code_generation_message = code_debagging_node.get_steamed_tokens()
            async for chunk in self.arun(
                question=question,
                code_generation_message=fixed_code_generation_message,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
                dependencies=dependencies,
                current_attempt=current_attempt + 1,
            ):
                yield chunk


code_execution_node = CodeExecutionNode(memory=agent_memory_service)
