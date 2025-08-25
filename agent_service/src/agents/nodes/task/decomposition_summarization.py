""" """

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.task.decomposition_summarization import (
    TaskDecompositionSummarizationPrompt,
)
from agents.models.anthropic_ import high_temp_model


class TaskDecompositionSummarizationNode(BaseNode):
    """..."""

    @override
    def invoke(self, state: AgentState):
        """..."""

        print("* TaskDecompositionSummarizationNode -> ")
        self._chain.invoke({"subtasks": state.subtasks})


class TaskDecompositionSummarizationNodeRegistry:

    TECHNICAL_MODE: TaskDecompositionSummarizationNode = (
        TaskDecompositionSummarizationNode(
            model=high_temp_model,
            prompt=TaskDecompositionSummarizationPrompt.TECHNICAL_MODE,
        )
    )

    QUICK_ANALYSIS_MODE: TaskDecompositionSummarizationNode = (
        TaskDecompositionSummarizationNode(
            model=high_temp_model,
            prompt=TaskDecompositionSummarizationPrompt.QUICK_ANALYSIS_MODE,
        )
    )
