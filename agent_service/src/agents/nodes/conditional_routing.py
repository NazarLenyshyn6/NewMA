"""
This module defines the `ConditionalRoutingNode` class, which provides routing logic
between different nodes of the AI agent's workflow. It determines the next execution
path based on the current agent state, task flow, subtask type, code execution results,
and debugging attempts.

The routing functions encapsulate conditional branching for:
- High-level task routing (advisory vs. solution flows).
- Subtask classification (analysis vs. visualization).
- Code execution success/failure with retry logic.
- Report generation and visualization handling.
- Direct responses and memory saving.

Classes:
    ConditionalRoutingNode: Encapsulates static methods for conditional routing
                            between nodes in the agent workflow.
"""

from agents.state import AgentState


class ConditionalRoutingNode:
    """
    Provides routing logic for transitioning between workflow nodes in the agent system.
    All routing decisions are made based on the current `AgentState`, ensuring dynamic
    flow control across different phases of analysis, visualization, debugging, and
    memory management.
    """

    @staticmethod
    def routing_from_agent_mode_classifier(state: AgentState):
        """
        Route from the agent mode classifier to the appropriate agent execution node.

        Args:
            state: The current agent state containing the `agent_mode`.

        Returns:
            str: The identifier of the next node:
                - "technical_agent" if `agent_mode` is TECHNICAL.
                - "quick_analysis_agent" otherwise.
        """
        if state.agent_mode == "TECHNICAL":
            return "technical_agent"
        return "quick_analysis_agent"

    @staticmethod
    def routing_from_task_router(state: AgentState):
        """
        Route from the task router to either advisory or decomposition flow.

        Args:
            state (AgentState): The current agent state containing the task flow type.

        Returns:
            str: The identifier of the next node ("context_advisor" or "task_decomposer").
        """
        if state.task_flow == "ADVISORY":
            return "context_advisor"
        return "task_decomposer"

    @staticmethod
    def routing_from_subtask_classifier(state: AgentState):
        """
        Route based on subtask classification to the appropriate action planner.

        Args:
            state (AgentState): The current agent state containing the subtask flow type.

        Returns:
            str: The identifier of the next node ("analysis_action_planner",
                 "visualization_action_planner", or "direct_responder").
        """
        if state.subtask_flow == "ANALYSIS":
            return "analysis_action_planner"
        elif state.subtask_flow == "VISUALIZATION":
            return "visualization_action_planner"
        return "direct_responder"

    @staticmethod
    def routing_from_code_executor(state: AgentState):
        """
        Route after code execution depending on success or failure.

        Args:
            state (AgentState): The current agent state containing error details
                                and debugging attempt counters.

        Returns:
            str: The identifier of the next node ("analysis_report_generator",
                 "visualization_display", "code_debugger", or "fallback_handler").
        """
        if state.error_message is None:
            if state.subtask_flow == "ANALYSIS":
                return "analysis_report_generator"
            return "visualization_display"
        else:
            if state.current_debugging_attempt <= state.max_debugging_attempts:
                return "code_debugger"
            return "fallback_handler"

    @staticmethod
    def routing_from_analysis_report_generator(state: AgentState):
        """
        Route after generating an analysis report. If subtasks remain,
        continue with classification; otherwise, save to memory.

        Args:
            state (AgentState): The current agent state containing remaining subtasks.

        Returns:
            str: The identifier of the next node ("subtask_classifier" or "memory_saver").
        """
        if len(state.subtasks) != 0:
            return "subtask_classifier"
        return "memory_saver"

    @staticmethod
    def routing_from_visualization_display(state: AgentState):
        """
        Route after visualization display. If subtasks remain,
        continue with classification; otherwise, save to memory.

        Args:
            state (AgentState): The current agent state containing remaining subtasks.

        Returns:
            str: The identifier of the next node ("subtask_classifier" or "memory_saver").
        """
        if len(state.subtasks) != 0:
            return "subtask_classifier"
        return "memory_saver"

    @staticmethod
    def routing_from_direct_responder(state: AgentState):
        """
        Route after directly responding to the user. If subtasks remain,
        continue with classification; otherwise, save to memory.

        Args:
            state (AgentState): The current agent state containing remaining subtasks.

        Returns:
            str: The identifier of the next node ("subtask_classifier" or "memory_saver").
        """
        if len(state.subtasks) != 0:
            return "subtask_classifier"
        return "memory_saver"
