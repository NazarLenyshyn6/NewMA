"""
Memory Retrieval Node Module.

This module defines the `MemoryRetrievalNode` class, responsible for
retrieving and populating various summaries and variables from persistent
memory into the agent's execution state. It provides a set of static
methods to safely interact with the `AgentState` and memory service,
allowing for consistent and modular state updates.

Responsibilities:
    - Retrieve analysis, visualization, code, and user preference summaries.
    - Retrieve stored variables associated with an agent session.
    - Provide utility methods for updating conversation state (questions and answers).
    - Encapsulate all memory interaction logic in a single reusable component.

This module is intended to be used as a helper in agent workflows,
ensuring clean separation between memory access and other node logic.
"""

import pickle

from agents.state import AgentState
from services.memory import memory_service


class MemoryRetrievalNode:
    """
    Node for retrieving and updating agent memory.

    `MemoryRetrievalNode` provides static helper methods to load summaries,
    variables, and conversation data from persistent memory into an
    `AgentState`. It abstracts away direct memory service calls, ensuring
    consistent usage across different agent nodes.

    All methods are static since memory retrieval does not depend on
    instance-specific state.
    """

    @staticmethod
    def get_analysis_summary(state: AgentState):
        """
        Load and attach the user's analysis summary to the agent state.

        Args:
            state (AgentState): The current agent execution state.
        """
        if state.analysis_report is None:
            state.analysis_summary = pickle.loads(
                memory_service.get_memory(
                    db=state.db,
                    user_id=state.user_id,
                    session_id=state.session_id,
                    file_name=state.file_name,
                    storage_uri=state.storage_uri,
                ).analysis_summary
            )

    @staticmethod
    def get_visualization_summary(state: AgentState):
        """
        Load and attach the user's visualization summary to the agent state.

        Args:
            state (AgentState): The current agent execution state.
        """
        if state.visualization_summary is None:
            state.visualization_summary = pickle.loads(
                memory_service.get_memory(
                    db=state.db,
                    user_id=state.user_id,
                    session_id=state.session_id,
                    file_name=state.file_name,
                    storage_uri=state.storage_uri,
                ).visualization_summary
            )

    @staticmethod
    def get_code_summary(state: AgentState):
        """
        Load and attach the user's code summary to the agent state.

        Args:
            state (AgentState): The current agent execution state.
        """
        if state.code_summary is None:
            state.code_summary = pickle.loads(
                memory_service.get_memory(
                    db=state.db,
                    user_id=state.user_id,
                    session_id=state.session_id,
                    file_name=state.file_name,
                    storage_uri=state.storage_uri,
                ).code_summary
            )

    @staticmethod
    def get_user_preferences_summary(state: AgentState):
        """
        Load and attach the user's preferences summary to the agent state.

        Args:
            state (AgentState): The current agent execution state.
        """
        if state.user_preferences_summary is None:
            state.user_preferences_summary = pickle.loads(
                memory_service.get_memory(
                    db=state.db,
                    user_id=state.user_id,
                    session_id=state.session_id,
                    file_name=state.file_name,
                    storage_uri=state.storage_uri,
                ).user_preferences_summary
            )

    @staticmethod
    def get_variables(state: AgentState):
        """
        Load and attach stored variables to the agent state.

        Args:
            state (AgentState): The current agent execution state.
        """
        if state.variables is None:
            state.variables = pickle.loads(
                memory_service.get_memory(
                    db=state.db,
                    user_id=state.user_id,
                    session_id=state.session_id,
                    file_name=state.file_name,
                    storage_uri=state.storage_uri,
                ).variables
            )

    @staticmethod
    def add_question(state: AgentState, question: str):
        """
        Add a question to the current new conversation in the agent state.

        Args:
            state (AgentState): The current agent execution state.
            question (str): The question text to record.
        """
        state.new_conversation[0]["question"] = question

    @staticmethod
    def add_answer(state: AgentState, answer: str):
        """
        Append an answer to the current new conversation in the agent state.

        Args:
            state (AgentState): The current agent execution state.
            answer (str): The answer text to append.
        """
        state.new_conversation[0]["answer"] = (
            state.new_conversation[0]["answer"] + answer
        )
