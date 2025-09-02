"""
Fallback Handling Node Module.

This module defines the `FallbackHandlingNode` and `FallbackHandlingNodeRegistry`
classes, which are responsible for generating fallback responses for subtasks
within the AI agent system.

Core responsibilities:
    - Use a high-temperature language model to generate fallback responses for
      subtasks that cannot be confidently executed.
    - Summarize pending context based on the generated fallback to maintain
      incremental state.
    - Record fallback responses in memory for future retrieval.
    - Provide preconfigured node instances for different agent modes (e.g., UNIFIED).
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.fallback_handling import FallbackHandlingPrompt
from agents.models.anthropic_ import high_temp_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode
from agents.nodes.summarization import SummarizationNode


class FallbackHandlingNode(BaseNode):
    """
    Executes fallback handling when the agent cannot confidently process a subtask.

    This node generates a fallback answer for a given subtask using a high-temperature
    language model, updates the pending context summary, and stores the answer in memory
    for future retrieval.

    Attributes:
        _chain: The execution chain integrating the model, prompt, and output logic.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Handle the current subtask by generating a fallback response, updating context,
        and storing it in memory.

        Args:
            state: The current agent state, which includes:
                - subtasks: Queue of subtasks derived from decomposition.
                - question: The original user question.
                - pending_context: Any pending context awaiting confirmation or execution.

        Returns:
            AgentState: The updated agent state with pending context summarized
                        and fallback answer added to memory.
        """
        ...

        # Generate a fallback answer for the first subtask
        fallback = self._chain.invoke({"question": state.subtasks[0]}).content

        # Summarize the pending context based on the generated fallback
        SummarizationNode.pending_context_summarization(
            state, state.question, fallback, state.pending_context
        )

        # Store the fallback answer in memory for conversation history
        MemoryRetrievalNode.add_answer(state, fallback)

        return state


class FallbackHandlingNodeRegistry:
    """
    Registry of preconfigured `FallbackHandlingNode` instances.

    Provides nodes specialized for different agent modes:
        - UNIFIED: Node configured for fallback handling using high-temperature LLM.

    Attributes:
        UNIFIED (FallbackHandlingNode): Node preconfigured for fallback handling.
    """

    # Node configured for high-temperature fallback handling
    UNIFIED: FallbackHandlingNode = FallbackHandlingNode(
        model=high_temp_model, prompt=FallbackHandlingPrompt.UNIFIED
    )
