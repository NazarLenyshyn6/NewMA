"""
This module defines the `VisualizationActionPlaningNode` and
`VisualizationActionPlaningNodeRegistry` classes, which are responsible for
generating visualization action plans within the AI agent system.

Core responsibilities:
    - Use a language model to propose a structured visualization plan.
    - Incorporate the first subtask and the visualization summary as input context.
    - Provide preconfigured node instances for different agent modes
      (technical vs. quick visualization).
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.visualization.action_planing import VisualizationActionPlaningPrompt
from agents.models.anthropic_ import medium_temp_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class VisualizationActionPlaningNode(BaseNode):
    """
    Executes action planning for visualization subtasks using a language model.

    This node generates a structured plan of action for how visualizations should
    be created, based on the current visualization summary and the first available subtask.

    Attributes:
        _chain: The execution chain that integrates the model,
                        prompt, and output handling logic.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Run the visualization action planning process on the current agent state.

        Args:
            state: The current state of the agent, which includes:
                - subtasks: A list of subtasks derived from decomposition.
                - visualization_summary: A summary of prior visualization steps.

        Returns:
            AgentState: The updated state object with the `visualization_action_plan`
            attribute populated based on the generated visualization plan.
        """
        print("* VisualizationActionPlaningNode -> ")

        # Use the first subtask and prior visualization summary to guide planning
        state.visualization_action_plan = self._chain.invoke(
            {
                "subtask": state.subtasks[0],
                "visualization_summary": state.visualization_summary,
            }
        ).content

        # Record visualization plan in memory for conversation history
        MemoryRetrievalNode.add_answer(state, state.visualization_action_plan)

        return state


class VisualizationActionPlaningNodeRegistry:
    """
    Registry of preconfigured `VisualizationActionPlaningNode` instances.

    Provides specialized nodes that adapt the visualization action planning process
    for different agent modes:
        - TECHNICAL_MODE: Produces a detailed, methodical visualization plan.
        - QUICK_VISUALIZATION_MODE: Produces a lightweight, rapid visualization plan.

    Attributes:
        TECHNICAL_MODE: Node configured for
            detailed technical visualization planning.
        QUICK_VISUALIZATION_MODE: Node configured
            for lightweight quick visualization planning.
    """

    # Node for detailed technical visualization planning
    TECHNICAL_MODE: VisualizationActionPlaningNode = VisualizationActionPlaningNode(
        model=medium_temp_model, prompt=VisualizationActionPlaningPrompt.TECHNICAL_MODE
    )

    # Node for quick and lightweight visualization planning
    QUICK_VISUALIZATION_MODE: VisualizationActionPlaningNode = (
        VisualizationActionPlaningNode(
            model=medium_temp_model,
            prompt=VisualizationActionPlaningPrompt.QUICK_VISUALIZATION_MODE,
        )
    )
