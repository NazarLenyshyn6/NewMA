"""
This module defines the `ContextAdvisingNode` and `ContextAdvisingNodeRegistry`
classes, which are responsible for generating contextual advice in the AI agent
system based on the current analysis and visualization summaries.

Core responsibilities:
    - Use a language model to generate context-aware advice for the user’s question.
    - Update the agent’s analysis summary with the generated advice.
    - Record the generated advice in memory for future reference.
    - Provide preconfigured node instances for different agent modes
      (technical vs. quick analysis).
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.context_advising import ContextAdvisingPrompt
from agents.models.anthropic_ import high_temp_model
from agents.nodes.summarization import SummarizationNode
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class ContextAdvisingNode(BaseNode):
    """
    Generates context-aware advice using a language model.

    This node takes the agent’s question along with the current analysis
    and visualization summaries, generates advice, updates the analysis
    summary, and records the advice in memory.

    Attributes:
        _chain: The execution chain that integrates the model,
                        prompt, and output handling logic.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Generate context-aware advice and update the agent state.

        Args:
            state: The current state of the agent, which includes:
                - question: The user’s original query.
                - analysis_summary: Current analysis summary.
                - visualization_summary: Current visualization summary.

        Returns:
            AgentState: The updated state with the generated advice included
                        in the analysis summary and recorded in memory.
        """
        print("* ContextAdvisingNode -> ")

        # Generate contextual advice using the model chain
        context_advise = self._chain.invoke(
            {
                "question": state.question,
                "analysis_summary": state.analysis_summary,
                "visualization_summary": state.visualization_summary,
                "pending_context": state.pending_context,
            }
        ).content

        # Update the analysis summary with the generated advice
        SummarizationNode.analysis_summarization(
            state, context_advise, state.analysis_summary
        )

        # Update pending context with new suggestion and question
        SummarizationNode.pending_context_summarization(
            state, state.question, context_advise, state.pending_context
        )

        # Record the generated advice in memory for conversation history
        MemoryRetrievalNode.add_answer(state, context_advise)

        return state


class ContextAdvisingNodeRegistry:
    """
    Registry of preconfigured `ContextAdvisingNode` instances.

    Provides nodes specialized for different agent modes:
        - TECHNICAL_MODE: Produces detailed, technical context advice.
        - QUICK_ANALYSIS_MODE: Produces concise, quick context advice.

    Attributes:
        TECHNICAL_MODE: Node for technical context advice.
        QUICK_ANALYSIS_MODE: Node for quick context advice.
    """

    # Node for detailed technical context advice
    TECHNICAL_MODE: ContextAdvisingNode = ContextAdvisingNode(
        model=high_temp_model, prompt=ContextAdvisingPrompt.TECHNICAL_MODE
    )

    # Node for quick beginner friendly context advice
    QUICK_ANALYSIS_MODE: ContextAdvisingNode = ContextAdvisingNode(
        model=high_temp_model, prompt=ContextAdvisingPrompt.QUICK_ANALYSIS_MODE
    )
