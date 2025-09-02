"""
This module defines the `TaskDecompositionSummarizationNode` and
`TaskDecompositionSummarizationNodeRegistry` classes, which are responsible
for summarizing task decompositions in an AI agent system.

Core responsibilities:
    - Use a language model to summarize subtasks generated during task
      decomposition.
    - Support multiple operational modes (e.g., technical, quick analysis)
      via preconfigured node instances in the registry.
    - Integrate seamlessly with the agent's state management system
      to access subtasks and store summaries.

Classes:
    - TaskDecompositionSummarizationNode: Encapsulates the logic for invoking
      task decomposition summarization using a specified model and prompt.
    - TaskDecompositionSummarizationNodeRegistry: Provides preconfigured node
      instances for different operational modes of the summarization process.
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.task.decomposition_summarization import (
    TaskDecompositionSummarizationPrompt,
)
from agents.models.anthropic_ import high_temp_model


class TaskDecompositionSummarizationNode(BaseNode):
    """
    Node responsible for summarizing task decompositions.

    This node interacts with a language model to generate summaries
    of subtasks. It is designed to work with an `AgentState` object
    and produce outputs that can guide subsequent agent actions.

    Methods:
        - invoke(state: AgentState):
            Processes the current agent state to generate and log
            a summarized decomposition of tasks.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Invoke the task decomposition summarization process.

        Args:
            state (AgentState): The current state of the agent,
                including a list of subtasks to summarize.

        Behavior:
            - Prints a log message indicating the node invocation.
            - Invokes the summarization chain with the subtasks
              from the provided agent state.
        """

        print("* TaskDecompositionSummarizationNode -> ")
        self._chain.invoke({"subtasks": state.subtasks})


class TaskDecompositionSummarizationNodeRegistry:
    """
    Registry providing preconfigured instances of
    TaskDecompositionSummarizationNode for different operational modes.

    Attributes:
        - TECHNICAL_MODE (TaskDecompositionSummarizationNode):
            Node configured for deep technical summarization.
        - QUICK_ANALYSIS_MODE (TaskDecompositionSummarizationNode):
            Node configured for rapid summarization suitable for
            high-level analysis.
    """

    # Preconfigured node for technical mode summarization
    TECHNICAL_MODE: TaskDecompositionSummarizationNode = (
        TaskDecompositionSummarizationNode(
            model=high_temp_model,
            prompt=TaskDecompositionSummarizationPrompt.TECHNICAL_MODE,
        )
    )

    # Preconfigured node for quick analysis summarization
    QUICK_ANALYSIS_MODE: TaskDecompositionSummarizationNode = (
        TaskDecompositionSummarizationNode(
            model=high_temp_model,
            prompt=TaskDecompositionSummarizationPrompt.QUICK_ANALYSIS_MODE,
        )
    )
