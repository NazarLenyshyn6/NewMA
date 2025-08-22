"""..."""

from typing import Any
from pydantic import BaseModel, PrivateAttr
from langgraph.graph import StateGraph, START, END


from agents.nodes.request_router import request_routing_node
from agents.nodes.suggestion import SuggestionNode, expert_suggestion_node
from agents.nodes.solution_planing import (
    SolutionPlaningNode,
    expert_solution_planing_node,
)
from agents.nodes.execution_planing import (
    ExecutionPlaningNode,
    expert_execution_planing_node,
)
from agents.nodes.code.mode_router import (
    code_mode_router_node,
)
from agents.nodes.code.generation.code_mode import (
    CodeGenNode,
    expert_code_gen_node,
)
from agents.nodes.code.generation.visualization_mode import (
    VisualizationGenNode,
    expert_visualization_gen_node,
)
from agents.nodes.code.debagging import (
    CodeDebaggingNode,
    expert_code_debagging_node,
)
from agents.nodes.save_memory import SaveMemoryNode
from agents.nodes.reporting import ReportingNode, expert_reporting_node
from agents.nodes.code.execution import CodeExecutionNode
from agents.nodes.routing.request_router import routing_from_requst_router_node
from agents.nodes.routing.code.mode_router import routing_from_code_mode_router
from agents.nodes.routing.code.execution import routing_from_code_execution_node
from agents.nodes.routing.reporting import routing_from_reporting_node
from agents.state import AgentState


class GraphBuilder(BaseModel):
    """..."""

    state_schema: type[BaseModel]
    suggestion_node: SuggestionNode
    solution_planing_node: SolutionPlaningNode
    execution_planing_node: ExecutionPlaningNode
    code_gen_node: CodeGenNode
    visualization_gen_node: VisualizationGenNode
    code_debagging_node: CodeDebaggingNode
    reporting_node: ReportingNode

    _graph = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._graph = StateGraph(self.state_schema)

    def _add_nodes(self):
        """..."""

        self._graph.add_node("request_routing", request_routing_node.route)
        self._graph.add_node("suggestion", self.suggestion_node.suggest)
        self._graph.add_node("solution_planing", self.solution_planing_node.plan)
        self._graph.add_node("execution_planing", self.execution_planing_node.plan)
        self._graph.add_node("code_mode_routing", code_mode_router_node.route)
        self._graph.add_node("visulization_gen", self.visualization_gen_node.generate)
        self._graph.add_node("code_gen", self.code_gen_node.generate)
        self._graph.add_node("code_execution", CodeExecutionNode.execute)
        self._graph.add_node("code_debagging", self.code_debagging_node.debug)
        self._graph.add_node("reporting", self.reporting_node.report)
        self._graph.add_node("fallback", lambda state: state)
        self._graph.add_node("save_memory", SaveMemoryNode.save)

    def _add_edges(self):
        """..."""
        self._graph.add_edge(START, "request_routing")
        self._graph.add_edge("suggestion", "save_memory")
        self._graph.add_edge("solution_planing", "execution_planing")
        self._graph.add_edge("execution_planing", "code_mode_routing")
        self._graph.add_edge("code_gen", "code_execution")
        self._graph.add_edge("visulization_gen", "code_execution")
        self._graph.add_edge("code_debagging", "code_execution")
        self._graph.add_edge("fallback", END)
        self._graph.add_edge("save_memory", END)

    def _add_conditional_edges(self):
        """..."""
        self._graph.add_conditional_edges(
            "request_routing",
            routing_from_requst_router_node,
            {"suggestion": "suggestion", "solution_planing": "solution_planing"},
        )
        self._graph.add_conditional_edges(
            "code_mode_routing",
            routing_from_code_mode_router,
            {"visulization_gen": "visulization_gen", "code_gen": "code_gen"},
        )
        self._graph.add_conditional_edges(
            "code_execution",
            routing_from_code_execution_node,
            {
                "fallback": "fallback",
                "code_debagging": "code_debagging",
                "reporting": "reporting",
            },
        )
        self._graph.add_conditional_edges(
            "reporting",
            routing_from_reporting_node,
            {"save_memory": "save_memory", "execution_planing": "execution_planing"},
        )

    def build(self):
        """..."""
        self._add_nodes()
        self._add_edges()
        self._add_conditional_edges()

        return self._graph.compile()


expert_agent = GraphBuilder(
    state_schema=AgentState,
    suggestion_node=expert_suggestion_node,
    solution_planing_node=expert_solution_planing_node,
    execution_planing_node=expert_execution_planing_node,
    code_gen_node=expert_code_gen_node,
    visualization_gen_node=expert_visualization_gen_node,
    code_debagging_node=expert_code_debagging_node,
    reporting_node=expert_reporting_node,
).build()
