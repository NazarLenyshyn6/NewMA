"""
This module defines the `CodeDebuggingNode` and `CodeDebuggingNodeRegistry`
classes, which are responsible for debugging Python code within the AI agent system.

Core responsibilities:
    - Use a language model to analyze and correct code based on the error message,
      previous code summary, and variable context.
    - Track the number of debugging attempts.
    - Record updated code in memory for future retrieval.
    - Provide preconfigured node instances for standardized usage.
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.code_debagging import CodeDebuggingPrompt
from agents.models.anthropic_ import code_debugging_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class CodeDebuggingNode(BaseNode):
    """
    Executes code debugging using a language model.

    This node takes the current agent state (including the user question, code,
    error message, code summary, and variable context) and invokes a debugging
    chain. The resulting corrected code is stored back in the state and recorded
    in memory.

    Attributes:
        _chain: The execution chain that integrates the model,
                        prompt, and output handling logic.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Perform code debugging on the current agent state and update memory.

        Args:
            state: The current state of the agent, which includes:
                - question: The user’s original query or description of the task.
                - code: The current code snippet to be debugged.
                - error_message: Error message received from code execution.
                - code_summary: Summary of previously generated code.
                - variables: Variables and their descriptions.

        Returns:
            None: The method updates `state.code`, increments debugging attempts,
                  and stores the updated code in memory.
        """

        print("* CodeDebaggingNode -> ")

        # Generate corrected code based on current code, error message, and context
        state.code = self._chain.invoke(
            {
                "question": state.subtasks[0],
                "dependencies": state.dependencies,
                "dataset_summary": state.dataset_summary,
                "code": state.code,
                "error_message": state.error_message,
                "code_summary": state.code_summary,
                "variables": state.variables.keys(),
            }
        ).content

        # Increment the debugging attempt counter
        state.current_debugging_attempt = state.current_debugging_attempt + 1

        # Record the updated code in memory for tracking
        MemoryRetrievalNode.add_answer(state, state.code)

        return state


class CodeDebaggingNodeRegistry:
    """
    Registry of preconfigured `CodeDebuggingNode` instances.

    Provides a unified node for standardized code debugging across tasks.

    Attributes:
        UNIFIED (CodeDebuggingNode): Node configured for unified debugging mode.
    """

    # Preconfigured node for unified code debuggings
    UNIFIED: CodeDebuggingNode = CodeDebuggingNode(
        model=code_debugging_model, prompt=CodeDebuggingPrompt.UNIFIED
    )
