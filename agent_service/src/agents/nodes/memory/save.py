"""
This module defines the `MemorySaveNode` class, which is responsible for
persisting the AI agent’s state into a memory service. It handles saving
analysis summaries, visualization summaries, code summaries, variables, and
conversation history for future retrieval and continuity across sessions.
"""

import pickle
from agents.state import AgentState
from services.memory import memory_service


class MemorySaveNode:
    """
    Node for saving the agent’s state and conversation into persistent memory.

    Responsibilities:
        - Retrieve existing conversation memory from storage.
        - Merge new conversation entries with existing conversation history.
        - Update the memory cache with current analysis, visualization, code,
          variables, and conversation data.
    """

    @staticmethod
    def invoke(state: AgentState) -> AgentState:
        """
        Save the current agent state and conversation history to the memory service.

        Args:
            state: The current state of the agent, which includes:
                - db: Database connection or reference.
                - user_id: Unique identifier for the user.
                - session_id: Current session identifier.
                - file_name: File name associated with the session or task.
                - storage_uri: Storage location for memory persistence.
                - analysis_summary: Current summary of analysis.
                - visualization_summary: Current summary of visualizations.
                - code_summary: Summary of generated code.
                - variables: Variables generated or updated in the session.
                - new_conversation: Newly generated conversation entries.

        Returns:
            AgentState: The updated state after saving memory.
        """

        print("* MemorySaveNode -> ")

        # Retrieve existing conversation memory
        conversation = memory_service.get_conversation_memory(
            db=state.db,
            user_id=state.user_id,
            session_id=state.session_id,
            file_name=state.file_name,
            storage_uri=state.storage_uri,
        )

        # Update the memory cache with current summaries, variables, and conversation
        memory_service.update_memory_cache(
            db=state.db,
            user_id=state.user_id,
            session_id=state.session_id,
            file_name=state.file_name,
            storage_uri=state.storage_uri,
            analysis_summary=(
                pickle.dumps(state.analysis_summary) if state.analysis_summary else None
            ),
            visualization_summary=(
                pickle.dumps(state.visualization_summary)
                if state.visualization_summary
                else None
            ),
            code_summary=(
                pickle.dumps(state.code_summary) if state.code_summary else None
            ),
            pending_context=(
                pickle.dumps(state.pending_context)
                if state.pending_context
                else pickle.dumps(f"Last Question\n: {state.question}")
            ),
            variables=pickle.dumps(state.variables) if state.variables else None,
            conversation=pickle.dumps(conversation + state.new_conversation),
        )

        return state
