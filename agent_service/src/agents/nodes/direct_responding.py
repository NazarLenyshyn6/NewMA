"""
This module defines the `DirectRespondingNode` and `DirectRespondingNodeRegistry`
classes, which are responsible for generating direct responses to subtasks
within the AI agent system.

Core responsibilities:
    - Use a language model to generate responses based on the first subtask
      and prior summaries of analysis and visualization.
    - Record generated responses in memory for conversation history.
    - Provide preconfigured node instances for different agent modes
      (technical vs. quick analysis).
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.direct_responding import DirectRespondingPrompt
from agents.models.anthropic_ import medium_temp_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class DirectRespondingNode(BaseNode):
    """
    Executes direct responding for subtasks using a language model.

    This node generates a direct response to a given subtask, taking into account
    the analysis and visualization summaries. It also logs the response into
    memory for future retrieval in the conversation history.

    Attributes:
        _chain: The execution chain that integrates the model,
                        prompt, and output handling logic.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Generate a direct response for the current subtask and update memory.

        Args:
            state: The current state of the agent, which includes:
                - subtasks: A list of subtasks derived from decomposition.
                - analysis_summary: Summary of prior analytical steps.
                - visualization_summary: Summary of prior visualization steps.

        Returns:
            None: The method updates memory and does not return a value.
        """

        print("* DirectRespondingNode -> ")

        # Generate a response for the first subtask using the model chain
        response = self._chain.invoke(
            {
                "subtask": state.subtasks[0],
                "analysis_summary": state.analysis_summary,
                "visualization_summary": state.visualization_summary,
            }
        ).content

        # Record response in memory for conversation history
        MemoryRetrievalNode.add_answer(state, response)

        # Remove the completed subtask from the queue
        state.subtasks.popleft()

        return state


class DirectRespondingNodeRegistry:
    """
    Registry of preconfigured `DirectRespondingNode` instances.

    Provides nodes specialized for different agent modes:
        - TECHNICAL_MODE: Produces detailed, technical responses.
        - QUICK_ANALYSIS_MODE: Produces rapid, concise responses.

    Attributes:
        TECHNICAL_MODE (DirectRespondingNode): Node configured for technical mode responses.
        QUICK_ANALYSIS_MODE (DirectRespondingNode): Node configured for quick analysis mode responses.
    """

    # Node for detailed technical direct responding
    TECHNICAL_MODE: DirectRespondingNode = DirectRespondingNode(
        model=medium_temp_model, prompt=DirectRespondingPrompt.TECHNICAL_MODE
    )

    # Node for quick and lightweight direct responding
    QUICK_ANALYSIS_MODE: DirectRespondingNode = DirectRespondingNode(
        model=medium_temp_model, prompt=DirectRespondingPrompt.QUICK_ANALYSIS_MODE
    )
