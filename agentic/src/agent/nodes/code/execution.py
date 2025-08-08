"""..."""

import re
from typing import override, Optional, List
from types import ModuleType
import importlib
from uuid import UUID
import pickle


from sqlalchemy.orm import Session

from agent.nodes.base import BaseNode
from services.memory import agent_memory_service
from agent.nodes.code.generation import dependencies


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
        code_generation_message: str,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
        dependencies: List[str] = dependencies,
    ):
        """..."""
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
            print(global_context)
            exec(code, global_context)
            local_context = {
                k: v
                for k, v in global_context.items()
                if k not in dependencies and not isinstance(v, ModuleType)
            }
            yield local_context
        except Exception as e:
            yield f"Code execution failed with error: {e}"


code_execution_node = CodeExecutionNode(memory=agent_memory_service)
