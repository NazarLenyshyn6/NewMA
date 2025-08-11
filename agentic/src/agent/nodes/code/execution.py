"""..."""

import re
from typing import override, Optional, List, Any
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
        pattern = r"```python\s([\s\S]*?)```"
        match = re.search(pattern, message.strip(), re.DOTALL)

        if not match:
            return None

        text = match.group(1).strip()
        return text

    @staticmethod
    def _is_pickle_serializable(obj: Any) -> bool:
        try:
            pickle.dumps(obj)
            return True
        except Exception:
            return False

    @override
    def run(
        self,
        question: str,
        dataset_summary: str,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
        code_debagging_node: CodeDebaggingNode = code_debagging_node,
    ): ...

    @override
    async def arun(
        self,
        question: str,
        code_generation_message: str,
        dataset_summary,
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
        if current_attempt == 1:
            self._token_buffer = []
        else:
            self._token_buffer.extend(code_debagging_node._token_buffer)

        if current_attempt > max_attempts:
            yield "Failed"
            return

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
                if self._is_pickle_serializable(v)
            }
            yield local_context

        except Exception as e:
            print("Error:", f"{e}")
            async for chunk in code_debagging_node.arun(
                question=question,
                dataset_summary=dataset_summary,
                code=code,
                error_message=f"{e}",
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
                dataset_summary=dataset_summary,
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
