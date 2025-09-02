"""
This module defines the `SubtaskClassificationNode` and `SubtaskClassificationNodeRegistry`
classes, which are responsible for classifying subtasks within the AI agent system.

Core responsibilities:
    - Use a language model to classify subtasks based on the user's question and prior context.
    - Incorporate analysis and visualization summaries to inform classification.
    - Provide preconfigured node instances for standardized usage.
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.subtask_classification import SubtaskClassificationPrompt
from agents.models.anthropic_ import low_temp_model


class SubtaskClassificationNode(BaseNode):
    """
    Executes subtask classification using a language model.

    This node takes the current agent state (including the user question, analysis summary,
    and visualization summary) and invokes a classification chain. The result is a
    structured subtask flow that guides subsequent agent execution.

    Attributes:
        _chain (Chain): The execution chain combining the model, prompt, and output parser.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Run the subtask classification process on the current agent state.

        Args:
            state: The current state of the agent, which includes:
                - question: The user’s original query.
                - analysis_summary: Summary of prior analytical steps.
                - visualization_summary: Summary of prior visualization steps.

        Returns:
            AgentState: The updated state object with the `subtask_flow` attribute populated
            based on the classification results.
        """
        print("* SubtaskClassificatoinNode -> ")

        # Invoke the chain with the question and prior summaries as context
        state.subtask_flow = self._chain.invoke(
            {
                "question": state.question,
                "analysis_summary": state.analysis_summary,
                "visualization_summary": state.visualization_summary,
                "pending_context": state.pending_context,
            },
            config={"metadata": {"stream": False}},
        ).content

        return state


class SubtaskClassificationNodeRegistry:
    """
    Registry of preconfigured `SubtaskClassificationNode` instances.

    Provides ready-to-use nodes for standardized subtask classification.

    Attributes:
        UNIFIED: Node configured for unified subtask classification.
    """

    # Preconfigured node for unified classification of subtasks
    UNIFIED: SubtaskClassificationNode = SubtaskClassificationNode(
        model=low_temp_model, prompt=SubtaskClassificationPrompt.UNIFIED
    )
