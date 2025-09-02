"""
This module defines the `TaskRoutingNode` and `TaskRoutingNodeRegistry` classes, which
are responsible for routing user questions to the appropriate task flow within an AI
agent system. It integrates memory retrieval for context-aware responses and leverages
an Anthropic language model with a predefined task routing prompt.

Classes:
    TaskRoutingNode: Executes task routing based on user input, analysis summaries,
                     visualization summaries, and user preference summaries.
    TaskRoutingNodeRegistry: Provides preconfigured instances of TaskRoutingNode for
                             different routing strategies.
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.task.routing import TaskRoutingPrompt
from agents.models.anthropic_ import low_temp_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class TaskRoutingNode(BaseNode):
    """
    Node responsible for routing a user's question to the appropriate task flow.

    This node combines information from:
        - Analysis summary
        - Visualization summary
        - User preferences summary

    It uses a language model and a task routing prompt to determine the best task flow.
    """

    @override
    def invoke(self, state: AgentState) -> AgentState:
        """
        Process the user's question and update the agent's task flow.

        Steps:
            1. Retrieve the latest analysis, visualization, and user preference summaries
               from memory.
            2. Invoke the language model with the question and context to determine
               the next task flow.
            3. Store the user's question in memory for conversation history.
            4. Update and return the agent state with the resolved task flow.

        Args:
            state (AgentState): Current state of the agent including question,
                                summaries, and other relevant context.

        Returns:
            AgentState: Updated agent state with the resolved task flow.
        """

        print("* TaskRoutingNode -> ")

        # Retrieve latest summaries from memory for context
        MemoryRetrievalNode.get_analysis_summary(state)
        MemoryRetrievalNode.get_visualization_summary(state)
        MemoryRetrievalNode.get_user_preferences_summary(state)
        MemoryRetrievalNode.get_pending_context(state)

        print("PENDING CONTEXT:", state.pending_context)

        # Invoke the task routing chain to determine the appropriate task flow
        state.task_flow = self._chain.invoke(
            {
                "question": state.question,
                "analysis_summary": state.analysis_summary,
                "visualization_summary": state.visualization_summary,
                "user_preferences_summary": state.user_preferences_summary,
                "pending_context": state.pending_context,
            },
            config={"metadata": {"stream": False}},
        ).content

        # Record the user's question in memory for conversation history
        MemoryRetrievalNode.add_question(state, state.question)

        return state


class TaskRoutingNodeRegistry:
    """
    Registry for preconfigured TaskRoutingNode instances.

    Provides convenient access to different task routing configurations.
    Currently includes:
        - UNIFIED: A TaskRoutingNode using the low temperature Anthropic model
                   and the unified task routing prompt.
    """

    UNIFIED: TaskRoutingNode = TaskRoutingNode(
        model=low_temp_model, prompt=TaskRoutingPrompt.UNIFIED
    )
