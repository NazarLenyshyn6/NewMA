"""
This module defines the `CodeExecutionNode` class, responsible for executing Python
code snippets within the AI agent system. It handles dependency imports, execution
in a controlled context, variable extraction, error handling, and updating the
agent state with results. It also integrates with the `SummarizationNode` to
summarize executed code.
"""

import re
import pickle
import importlib
from types import ModuleType
from typing import Optional, List, Any


from agents.state import AgentState
from agents.nodes.summarization import SummarizationNode


class CodeExecutionNode:
    """
    Executes Python code snippets in a controlled environment and updates agent state.

    Responsibilities:
        - Extract code from text (triple-backtick Python code blocks).
        - Import dependencies dynamically.
        - Execute code in a combined global and local context.
        - Track variables that are pickle-serializable for later retrieval.
        - Update agent state with execution results, errors, and summaries.
    """

    @staticmethod
    def _import_dependencies(dependencies: List[str]):
        """
        Dynamically import required Python packages.

        Args:
            dependencies: List of package/module names to import.

        Returns:
            dict: Mapping of package names to imported module objects.
        """
        imported_modules = {}
        for package_name in dependencies:
            try:
                module = importlib.import_module(package_name)
                imported_modules[package_name] = module
            except Exception:
                # Ignore import errors for missing packages
                ...
        return imported_modules

    @staticmethod
    def _is_pickle_serializable(obj: Any) -> bool:
        """
        Check if an object can be serialized with pickle.

        Args:
            obj (Any): Object to test for pickle serialization.

        Returns:
            bool: True if object can be pickled, False otherwise.
        """
        try:
            pickle.dumps(obj)
            return True
        except Exception:
            return False

    @staticmethod
    def _extract_code(message: str) -> Optional[str]:
        """
        Extract Python code from a triple-backtick code block in a message.

        Args:
            message: Text containing Python code wrapped in ```python ... ```.

        Returns:
            Optional[str]: Extracted code if present; otherwise, None.
        """
        pattern = r"```python\s([\s\S]*?)```"
        match = re.search(pattern, message.strip(), re.DOTALL)

        if not match:
            return None

        text = match.group(1).strip()
        return text

    @classmethod
    def invoke(cls, state: AgentState) -> AgentState:
        """
        Execute the code from the agent state and update variables, errors, and summaries.

        Args:
            state: The current state of the agent, containing:
                - code: Code snippet to execute.
                - dependencies: Required Python packages.
                - variables: Existing variables to include in execution.
                - subtask_flow: Current subtask flow ("ANALYSIS" or "VISUALIZATION").
                - code_summary: Previous code summaries.

        Returns:
            AgentState: Updated state with executed variables, error messages, and summaries.
        """

        print("* CodeExecutionNode -> ")

        # Extract the Python code block from the state
        code = cls._extract_code(state.code)

        # Prepare execution contexts
        global_context = cls._import_dependencies(
            state.dependencies
        )  # Imported modules

        local_context = state.variables.copy()  # Existing variables
        global_context.update(local_context)  # Merge contexts

        try:
            # Execute the code in combined context
            exec(code, global_context)

            # Extract only pickle-serializable variables, ignoring modules and dependencies
            variables = {
                k: v
                for k, v in global_context.items()
                if k not in state.dependencies and not isinstance(v, ModuleType)
                if cls._is_pickle_serializable(v)
            }

            state.variables = variables

            # Summarize executed code
            SummarizationNode.code_summarization(
                state, code, state.code_summary, state.variables
            )

            # Update subtask-specific outputs
            if state.subtask_flow == "ANALYSIS":
                state.analysis_report = state.variables.get("analysis_report")
            elif state.subtask_flow == "VISUALIZATION":
                state.visualization = state.variables.get("image")

            # Clear previous error messages and reset debagging attemps counter
            state.error_message = None
            state.current_debugging_attempt = 0

        except Exception as e:
            # Capture any execution errors
            state.error_message = f"{e}"

        finally:
            return state
