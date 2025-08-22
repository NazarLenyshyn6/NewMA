"""..."""

from agents.state import AgentState


def routing_from_code_execution_node(state: AgentState):
    if state.code_error is None:
        return "reporting"
    else:
        if state.current_code_debagging_attempt < state.max_code_debagging_attempts:
            return "code_debagging"
        return "fallback"
