"""
This module defines the `TaskDecompositionNode` and `TaskDecompositionNodeRegistry`
classes, which are responsible for breaking down complex user queries into structured
subtasks within the AI agent system.

Core responsibilities:
    - Use a language model to perform task decomposition.
    - Incorporate analysis and visualization context into decomposition.
    - Provide specialized node instances for different agent modes (technical vs. quick analysis).
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.task.decomposition import TaskDecompositionPrompt
from agents.models.anthropic_ import medium_temp_model
from agents.structured_outputs.task.decomposition import TaskDecompositionOutput


class TaskDecompositionNode(BaseNode):
    """
    Executes task decomposition using a language model and structured outputs.

    This node takes the current agent state (including the user question, analysis summary,
    and visualization summary) and invokes a task decomposition chain. The result is a set
    of structured subtasks.

    Attributes:
        _chain (Chain): The execution chain that wraps the model, prompt, and output parser.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Run the task decomposition process on the current agent state.

        Args:
            state: The current state of the agent, which includes:
                - question: The user’s original query.
                - analysis_summary: Summary of prior analytical steps.
                - visualization_summary (str): Summary of prior visualization steps.

        Returns:
            AgentState: The updated state object with the `subtasks` attribute populated
            based on the structured output from the decomposition process.
        """

        print("* TaskDecompositionNode -> ")

        # Invoke the chain with the user question and prior summaries as context
        state.subtasks = self._chain.invoke(
            {
                "question": state.question,
                "analysis_summary": state.analysis_summary,
                "visualization_summary": state.visualization_summary,
                "pending_context": state.pending_context,
            },
            config={"metadata": {"stream": False}},
        ).subtasks

        return state


class TaskDecompositionNodeRegistry:
    """
    Registry of preconfigured `TaskDecompositionNode` instances for different modes.

    Provides ready-to-use nodes that specialize the decomposition process for distinct
    agent modes:
        - TECHNICAL_MODE: Focuses on deeply technical decomposition of tasks.
        - QUICK_ANALYSIS_MODE: Provides a lightweight, fast decomposition for rapid insights.

    Attributes:
        TECHNICAL_MODE (TaskDecompositionNode): Node configured for technical analysis mode.
        QUICK_ANALYSIS_MODE (TaskDecompositionNode): Node configured for quick analysis mode.
    """

    # Node for detailed technical task decomposition
    TECHNICAL_MODE: TaskDecompositionNode = TaskDecompositionNode(
        model=medium_temp_model,
        prompt=TaskDecompositionPrompt.TECHNICAL_MODE,
        structured_output=TaskDecompositionOutput,
    )

    # Node for quick and lightweight task decomposition
    QUICK_ANALYSIS_MODE: TaskDecompositionNode = TaskDecompositionNode(
        model=medium_temp_model,
        prompt=TaskDecompositionPrompt.QUICK_ANALYSIS_MODE,
        structured_output=TaskDecompositionOutput,
    )
