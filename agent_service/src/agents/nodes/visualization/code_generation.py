"""
This module defines the `VisualizationCodeGenerationNode` and
`VisualizationCodeGenerationNodeRegistry` classes, which are responsible for
generating Python code for visualization tasks within the AI agent system.

Core responsibilities:
    - Use a language model to generate visualization code based on dependencies,
      dataset summaries, previous code summaries, and variables.
    - Incorporate the agent’s visualization action plan into code generation.
    - Record generated code in memory for tracking and future retrieval.
    - Provide preconfigured node instances for different agent modes
      (technical vs. quick visualization).
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.visualization.code_generation import (
    VisualizationCodeGenerationPrompt,
)
from agents.models.anthropic_ import code_generation_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class VisualizationCodeGenerationNode(BaseNode):
    """
    Generates Python code for visualization subtasks using a language model.

    This node retrieves necessary context (dependencies, dataset summary,
    code summary, and variables) from memory and uses it to generate
    code for the specified visualization action plan. The generated code is
    then stored in memory for future reference.

    Attributes:
        _chain: The execution chain that integrates the model,
                        prompt, and output handling logic.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Generate visualization code for the current subtask and update memory.

        Args:
            state: The current state of the agent, which includes:
                - dependencies: List of required library imports or dependencies.
                - dataset_summary: Summary of the dataset.
                - code_summary: Summary of previously generated code.
                - variables: Variables and their descriptions.
                - visualization_action_plan: Planned steps for visualization.

        Returns:
            AgentState: The updated state object with the `code`
                        attribute populated and memory updated.
        """
        print("* VisualizationCodeGenerationNode -> ")

        # Retrieve previous code summaries and variables from memory
        MemoryRetrievalNode.get_code_summary(state)
        MemoryRetrievalNode.get_variables(state)

        # Generate new visualization code based on dependencies, dataset, variables, and plan
        state.code = self._chain.invoke(
            {
                "dependencies": state.dependencies,
                "dataset_summary": state.dataset_summary,
                "code_summary": state.code_summary,
                "variables": state.variables.keys(),
                "visualization_action_plan": state.visualization_action_plan,
            }
        ).content

        # Record the generated code in memory for tracking
        MemoryRetrievalNode.add_answer(state, state.code)

        return state


class VisualizationCodeGenerationNodeRegistry:
    """
    Registry of preconfigured `VisualizationCodeGenerationNode` instances.

    Provides specialized nodes for different agent modes:
        - TECHNICAL_MODE: Produces detailed, methodical visualization code.
        - QUICK_VISUALIZATION_MODE: Produces lightweight, rapid visualization code.

    Attributes:
        TECHNICAL_MODE: Node configured for
            technical mode visualization code generation.
        QUICK_VISUALIZATION_MODE: Node configured for
            quick visualization code generation.
    """

    # Node for detailed technical visualization code generation
    TECHNICAL_MODE: VisualizationCodeGenerationNode = VisualizationCodeGenerationNode(
        model=code_generation_model,
        prompt=VisualizationCodeGenerationPrompt.TECHNICAL_MODE,
    )

    # Node for quick and lightweight visualization code generation
    QUICK_VISUALIZATION_MODE: VisualizationCodeGenerationNode = (
        VisualizationCodeGenerationNode(
            model=code_generation_model,
            prompt=VisualizationCodeGenerationPrompt.QUICK_VISUALIZATION_MODE,
        )
    )
