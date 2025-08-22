"""..."""

from agents.state import AgentState


def routing_from_requst_router_node(state: AgentState):
    if state.request_type == "SUGGESTION":
        return "suggestion"
    return "solution_planing"
