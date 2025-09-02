"""
This module defines the `AnalysisActionPlaningNode` and
`AnalysisActionPlaningNodeRegistry` classes, which are responsible for
generating an actionable analysis plan for a given subtask.

Core responsibilities:
    - Use a language model to propose a structured analysis action plan.
    - Incorporate the current analysis summary and the first subtask
      as input context.
    - Provide preconfigured node instances for different agent modes
      (technical vs. quick analysis).
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.analysis.action_planing import AnalysisActionPlaningPrompt
from agents.models.anthropic_ import medium_temp_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class AnalysisActionPlaningNode(BaseNode):
    """
    Executes action planning for analysis subtasks using a language model.

    This node generates a structured plan of action for how the analysis should
    proceed, based on the current analysis summary and the first available subtask.

    Attributes:
        _chain (Chain): The execution chain that integrates the model,
                        prompt, and output handling logic.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Run the analysis action planning process on the current agent state.

        Args:
            state: The current state of the agent, which includes:
                - subtasks: A list of subtasks derived from decomposition.
                - analysis_summary: A summary of prior analytical steps.

        Returns:
            AgentState: The updated state object with the `analysis_action_plan`
            attribute populated based on the generated plan.
        """

        print("* AnalysisActionPlaningNode -> ")
        print("ANALYSIS SUMMARY:", state.analysis_summary, "\n\n")

        # Use the first subtask and prior analysis summary to guide action planning
        state.analysis_action_plan = self._chain.invoke(
            {"subtask": state.subtasks[0], "analysis_summary": state.analysis_summary}
        ).content

        # Record analysis plan in memory for conversation history
        MemoryRetrievalNode.add_answer(state, state.analysis_action_plan)

        return state


class AnalysisActionPlaningNodeRegistry:
    """
    Registry of preconfigured `AnalysisActionPlaningNode` instances.

    Provides specialized nodes that adapt the action planning process
    for different agent modes:
        - TECHNICAL_MODE: Produces a detailed, methodical action plan.
        - QUICK_ANALYSIS_MODE: Produces a lightweight, rapid action plan.

    Attributes:
        TECHNICAL_MODE: Node configured for
            detailed technical action planning.
        QUICK_ANALYSIS_MODE: Node configured for
            lightweight quick analysis action planning.
    """

    # Node for detailed technical action planning
    TECHNICAL_MODE: AnalysisActionPlaningNode = AnalysisActionPlaningNode(
        model=medium_temp_model, prompt=AnalysisActionPlaningPrompt.TECHNICAL_MODEL
    )

    # Node for quick and lightweight action planning
    QUICK_ANALYSIS_MODE: AnalysisActionPlaningNode = AnalysisActionPlaningNode(
        model=medium_temp_model, prompt=AnalysisActionPlaningPrompt.QUICK_ANALYSIS_MODE
    )
