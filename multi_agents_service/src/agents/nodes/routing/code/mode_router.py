"""..."""

from agents.state import AgentState


def routing_from_code_mode_router(state: AgentState):
    if state.code_mode == "VISUALIZATION":
        return "visulization_gen"
    return "code_gen"
