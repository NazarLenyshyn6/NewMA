"""
This module defines the `AgentOrchestrationNode` and its registry for orchestrating
the overall behavior of the AI agent. It is responsible for determining the agent’s
operating mode (e.g., technical, quick analysis, or mentor) by combining the user’s
current query with a summarized view of their preferences.

Key Responsibilities:
    - Retrieve and incorporate user preference summaries from memory.
    - Use a language model with the unified orchestration prompt to infer the most
      appropriate agent mode.
    - Update the agent state with the selected mode for downstream task execution.

Classes:
    AgentOrchestrationNode: Executes orchestration logic to decide the agent’s
                            operational mode based on question context and user
                            preferences.
    AgentOrchestrationNodeRegistry: Provides preconfigured registry entries for
                                    agent orchestration, ensuring a unified
                                    orchestration pathway.
"""

from typing import override

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.agent_mode_classification import AgentModeClassificationPrompt
from agents.models.anthropic_ import low_temp_model
from agents.nodes.memory.retrieval import MemoryRetrievalNode
from agents.nodes.summarization import SummarizationNode


class AgentModeClassificationNode(BaseNode):
    """
    Node responsible for orchestrating the agent’s operational mode.

    This node retrieves the user’s preferences from memory and invokes the
    orchestration model with the unified prompt. The resulting mode is stored
    in the shared agent state, which guides downstream task execution
    (e.g., analysis, visualization, mentoring).

    Responsibilities:
        - Query memory for the latest user preference summary.
        - Invoke the orchestration model with question + preferences.
        - Update `state.agent_mode` with the chosen operational mode.
    """

    @override
    def invoke(self, state: AgentState):
        """
        Executes the orchestration process for determining the agent’s mode.

        Steps:
            1. Retrieves the latest user preference summary from memory.
            2. Calls the orchestration model with the current question and
               preference summary using the unified orchestration prompt.
            3. Updates `state.agent_mode` with the inferred mode.

        Args:
            state (AgentState): The current agent state, containing the
                                user’s question and storage for orchestration
                                results.

        Side Effects:
            - Updates `state.user_preferences_summary` with the latest
              memory retrieval.
            - Mutates `state.agent_mode` to reflect the chosen mode.

        Returns:
            None: The state is modified in place.
        """

        print("* AgentModeClassificationNode -> ")

        # Retrieve preferences from memory
        MemoryRetrievalNode.get_user_preferences_summary(state)

        # Invoke model and update stat
        state.agent_mode = self._chain.invoke(
            {
                "question": state.question,
                "user_preferences_summary": state.user_preferences_summary,
            },
            config={"metadata": {"stream": False}},
        ).content
        
        # Summarize user preferences
        SummarizationNode.user_preferences_summarization(state, state.question, state.user_preferences_summary)

        print("MODE:", state.agent_mode)
        print("USER PREFERENCES:", state.user_preferences_summary, "\n\n")

        return state


class AgentModeClassificationNodeRegistry:
    """
    Registry for accessing preconfigured orchestration nodes.

    This ensures consistent reuse of orchestration nodes across the agent system,
    centralizing the creation and configuration of nodes.

    Attributes:
        UNIFIED (AgentNodeClassificationNode): A default orchestration node configured
                                          with the unified orchestration prompt
                                          and low-temperature model for stable
                                          mode inference.
    """

    UNIFIED: AgentModeClassificationNode = AgentModeClassificationNode(
        model=low_temp_model, prompt=AgentModeClassificationPrompt.UNIFIED
    )
