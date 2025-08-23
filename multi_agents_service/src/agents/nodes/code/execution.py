"""..."""

import re
import importlib
from types import ModuleType
from typing import List, Any, Optional
import pickle

from agents.state import AgentState
from services.memory.variables import variables_memory_service
from agents.nodes.summarization import SummarizationNode


class CodeExecutionNode:

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
    def _is_pickle_serializable(obj: Any) -> bool:
        try:
            pickle.dumps(obj)
            return True
        except Exception:
            return False

    @staticmethod
    def _extract_code(message: str) -> Optional[str]:
        """..."""
        pattern = r"```python\s([\s\S]*?)```"
        match = re.search(pattern, message.strip(), re.DOTALL)

        if not match:
            return None

        text = match.group(1).strip()
        return text

    @classmethod
    def execute(cls, state: AgentState) -> AgentState:
        """..."""
        print("* CodeExecutionNode ->")

        # Set up enviroment for code execution
        code = cls._extract_code(state.code)
        global_context = cls._import_dependencies(state.dependencies)
        local_context = state.variables_memory.copy()
        global_context.update(local_context)
        try:
            exec(code, global_context)
            persisted_variables = {
                k: v
                for k, v in global_context.items()
                if k not in state.dependencies and not isinstance(v, ModuleType)
                if cls._is_pickle_serializable(v)
            }

            # Update code summary and variables memory, becaues code executed successfully
            state.variables_memory = persisted_variables
            state.code_summary_memory = SummarizationNode.code_summarization(
                code=state.code,
                code_summary_memory=state.code_summary_memory,
                variables_memory=state.variables_memory,
            )

            # Get data for reports
            if state.code_mode == "CODE":
                state.analysis_report = state.variables_memory.get("analysis_report")
            else:
                state.image = state.variables_memory.get("image")

            # Set error to None
            state.code_error = None

        except Exception as e:
            state.code_error = f"{e}"

        finally:
            return state
