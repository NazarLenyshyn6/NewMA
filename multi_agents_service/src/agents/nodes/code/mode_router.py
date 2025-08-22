"""..."""

from agents.nodes.base import BaseNode
from agents.prompts.code.mode_router import code_mode_routing_prompt
from agents.models.anthropic_ import code_mode_routing_model
from agents.state import AgentState


class CodeModeRouterNode(BaseNode):

    def route(self, state: AgentState) -> AgentState:
        """..."""
        state.code_mode = self._chain.invoke(
            {
                "question": state.execution_plan,
            },
            config={"metadata": {"stream": False}},
        ).content
        return state


code_mode_router_node = CodeModeRouterNode(
    model=code_mode_routing_model, prompt=code_mode_routing_prompt
)
