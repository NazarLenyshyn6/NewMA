"""..."""

from langgraph.graph import END

from agents.state import AgentState


def routing_from_reporting_node(state: AgentState):
    if len(state.subtasks) == 0:
        return "save_memory"
    return "execution_planing"
