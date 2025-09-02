"""
This module defines the `AnalysisCodeGenerationNode` and
`AnalysisCodeGenerationNodeRegistry` classes, which are responsible for
generating Python code for analysis tasks within the AI agent system.

Core responsibilities:
    - Use a language model to generate analysis code based on dependencies,
      dataset summaries, previous code summaries, and variables.
    - Incorporate the agent’s analysis action plan into code generation.
    - Record generated code in memory for tracking and future retrieval.
    - Provide preconfigured node instances for different agent modes
      (technical vs. quick analysis).
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.analysis.code_generation import AnalysisCodeGenerationPrompt
from agents.models.anthropic_ import code_generation_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class AnalysisCodeGenerationNode(BaseNode):
    """
    Generates Python code for analysis subtasks using a language model.

    This node retrieves necessary context (dependencies, dataset summary,
    code summary, and variables) from memory and uses it to generate
    code for the specified analysis action plan. The generated code is
    then stored in memory for future reference.

    Attributes:
        _chain: The execution chain that integrates the model,
                        prompt, and output handling logic.
    """

    ...

    @override
    def invoke(self, state: AgentState):
        """
        Generate analysis code for the current subtask and update memory.

        Args:
            state: The current state of the agent, which includes:
                - dependencies: List of required library imports or dependencies.
                - dataset_summary: Summary of the dataset.
                - code_summary: Summary of previously generated code.
                - variables: Variables and their descriptions.
                - analysis_action_plan: Planned steps for analysis.

        Returns:
            None: The method updates `state.code` and memory,
                  no value is returned.
        """

        print("* AnalysisCodeGenerationModel -> ")

        # Retrieve previous code summaries and variables from memory
        MemoryRetrievalNode.get_code_summary(state)
        MemoryRetrievalNode.get_variables(state)

        # Generate new analysis code based on dependencies, dataset, variables, and plan
        state.code = self._chain.invoke(
            {
                "dependencies": state.dependencies,
                "dataset_summary": state.dataset_summary,
                "code_summary": state.code_summary,
                "variables": state.variables.keys(),
                "analysis_action_plan": state.analysis_action_plan,
                "custom_data": state.question,
            }
        ).content

        # Record the generated code in memory for tracking
        MemoryRetrievalNode.add_answer(state, state.code)

        return state


class AnalysisCodeGenerationNodeRegistry:
    """
    Registry of preconfigured `AnalysisCodeGenerationNode` instances.

    Provides specialized nodes for different agent modes:
        - TECHNICAL_MODE: Produces detailed, methodical code generation.
        - QUICK_ANALYSIS_MODE: Produces lightweight, rapid code generation.

    Attributes:
        TECHNICAL_MODE: Node configured for
            technical mode code generation.
        QUICK_ANALYSIS_MODE: Node configured for
            quick analysis mode code generation.
    """

    # Node for detailed technical code generation
    TECHNICAL_MODE: AnalysisCodeGenerationNode = AnalysisCodeGenerationNode(
        model=code_generation_model, prompt=AnalysisCodeGenerationPrompt.TECHNICAL_MODE
    )

    # Node for quick and lightweight code generation
    QUICK_ANALYSIS_MODE: AnalysisCodeGenerationNode = AnalysisCodeGenerationNode(
        model=code_generation_model,
        prompt=AnalysisCodeGenerationPrompt.QUICK_ANALYSIS_MODE,
    )
