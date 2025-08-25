"""
Agents Orchestrator Graph Builder

This module defines the `AgentsOrchestratorGraphBuilder` class, which constructs and
compiles a workflow graph for orchestrating multiple AI agent modes (e.g., technical
analysis, quick analysis). The orchestrator integrates classification, conditional
routing, and execution nodes into a unified graph, enabling dynamic delegation of tasks
to specialized agents depending on the user’s needs.

Key Components:
    - AgentsOrchestratorGraphBuilder: Core builder class responsible for creating the
      agent orchestration graph.
    - agents_orchestrator: A pre-built instance of the orchestrator graph, ready for use.

Responsibilities:
    - Initialize a stateful graph with Pydantic-based state management.
    - Add classification, execution, and routing nodes.
    - Define static edges (deterministic execution flow).
    - Define conditional edges (dynamic routing based on agent mode classification).
    - Compile and return a fully executable workflow graph.
"""

from typing import Any, Type

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langgraph.graph import StateGraph, START, END

from agents.state import AgentState
from agents.nodes.agent_model_classification import (
    AgentModeClassificationNodeRegistry,
    AgentModeClassificationNode,
)
from agents.nodes.conditional_routing import ConditionalRoutingNode
from agents.graphs.builder import AgentGraphRegistry


class AgentsOrchestratorGraphBuilder(BaseModel):
    """
    Builder class for constructing an orchestrator graph that routes tasks between
    multiple AI agent modes.

    The orchestrator integrates:
        - A classification node to determine the correct agent mode.
        - Agent execution nodes (technical, quick analysis, etc.).
        - Conditional routing logic that directs workflow dynamically.

    Attributes:
        state: The agent state class to be tracked in the workflow.
        agent_mode_classification_node: The node
            responsible for classifying user input into a specific agent mode.
        _graph: The underlying execution graph (initialized post-init).
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    state: Type[BaseModel]
    agent_mode_classification_node: AgentModeClassificationNode

    _graph: StateGraph = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """
        Post-initialization hook to create a new StateGraph for the agent.

        Args:
            __context (Any): Context provided during Pydantic initialization.
        """
        self._graph = StateGraph(self.state)

    def _add_nodes(self):
        """
        Add classification and execution nodes to the graph.

        Nodes include:
            - agent_mode_classifier: Determines which agent mode should run.
            - technical_agent: Handles deeply technical analysis tasks.
            - quick_analysis_agent: Handles lightweight, quick analysis tasks.
        """
        self._graph.add_node(
            "agent_mode_classifier", self.agent_mode_classification_node.invoke
        )
        self._graph.add_node("technical_agent", AgentGraphRegistry.TECHNICAL_MODE)
        self._graph.add_node(
            "quick_analysis_agent", AgentGraphRegistry.QUICK_ANALYSIS_MODE
        )

    def _add_edges(self):
        """
        Add static edges between nodes to define execution order.

        These edges are unconditional and ensure the workflow progresses linearly
        through classification into execution, followed by termination.
        """
        self._graph.add_edge(START, "agent_mode_classifier")
        self._graph.add_edge("technical_agent", END)
        self._graph.add_edge("quick_analysis_agent", END)

    def _add_conditional_edges(self):
        """
        Add conditional edges to the state graph.

        Conditional edges allow branching logic based on classification results.
        The classifier's decision determines whether the workflow continues into
        the technical agent or the quick analysis agent.
        """
        self._graph.add_conditional_edges(
            "agent_mode_classifier",
            ConditionalRoutingNode.routing_from_agent_mode_classifier,
            {
                "technical_agent": "technical_agent",
                "quick_analysis_agent": "quick_analysis_agent",
            },
        )

    def build(self):
        """
        Build and compile the agent workflow graph.

        Returns:
            StateGraph: The compiled execution graph ready for use.
        """

        self._add_nodes()
        self._add_edges()
        self._add_conditional_edges()

        return self._graph.compile()


# Compiled instance of the orchestrator graph, ready for execution.
agents_orchestrator = AgentsOrchestratorGraphBuilder(
    state=AgentState,
    agent_mode_classification_node=AgentModeClassificationNodeRegistry.UNIFIED,
).build()
