"""
This module defines the `AgentGraphBuilder` and `AgentGraphRegistry` classes,
which construct and configure the execution graph for an AI agent workflow.

Core responsibilities:
    - Build a state-driven workflow graph for task routing, decomposition,
      subtask classification, action planning, code generation, and response.
    - Add nodes corresponding to individual agent operations.
    - Define edges and conditional edges to dictate execution flow.
    - Provide preconfigured agent graph instances for different modes:
        TECHNICAL_MODE and QUICK_ANALYSIS_MODE.
"""

from typing import Any, Type

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langgraph.graph import StateGraph, START, END

from agents.state import AgentState
from agents.nodes.task.routing import TaskRoutingNode, TaskRoutingNodeRegistry
from agents.nodes.task.decomposition import (
    TaskDecompositionNode,
    TaskDecompositionNodeRegistry,
)
from agents.nodes.subtask_classification import (
    SubtaskClassificationNode,
    SubtaskClassificationNodeRegistry,
)
from agents.nodes.context_advising import (
    ContextAdvisingNode,
    ContextAdvisingNodeRegistry,
)
from agents.nodes.direct_responding import (
    DirectRespondingNode,
    DirectRespondingNodeRegistry,
)
from agents.nodes.analysis.action_planing import (
    AnalysisActionPlaningNode,
    AnalysisActionPlaningNodeRegistry,
)
from agents.nodes.analysis.code_generation import (
    AnalysisCodeGenerationNode,
    AnalysisCodeGenerationNodeRegistry,
)
from agents.nodes.analysis.report_generation import (
    AnalysisReportGenerationNode,
    AnalysisReportGenerationNodeRegistry,
)
from agents.nodes.visualization.action_planing import (
    VisualizationActionPlaningNode,
    VisualizationActionPlaningNodeRegistry,
)
from agents.nodes.visualization.code_generation import (
    VisualizationCodeGenerationNode,
    VisualizationCodeGenerationNodeRegistry,
)
from agents.nodes.task.decomposition_summarization import (
    TaskDecompositionSummarizationNode,
    TaskDecompositionSummarizationNodeRegistry,
)
from agents.nodes.visualization.display import VisualizationDisplayNode
from agents.nodes.code.execution import CodeExecutionNode
from agents.nodes.code.debagging import CodeDebuggingNode, CodeDebaggingNodeRegistry
from agents.nodes.memory.save import MemorySaveNode
from agents.nodes.conditional_routing import ConditionalRoutingNode


class AgentGraphBuilder(BaseModel):
    """
    Builder for constructing an agent execution graph.

    Attributes:
        state (Type[BaseModel]): The agent's state class.
        task_routing_node (TaskRoutingNode): Node for routing tasks.
        task_decomposition_node (TaskDecompositionNode): Node for decomposing tasks.
        subtask_classification_node (SubtaskClassificationNode): Node for classifying subtasks.
        direct_responding_node (DirectRespondingNode): Node for generating direct responses.
        context_advising_node (ContextAdvisingNode): Node for providing contextual advice.
        analysis_action_planing_node (AnalysisActionPlaningNode): Node for planning analysis actions.
        analysis_code_generation_node (AnalysisCodeGenerationNode): Node for generating analysis code.
        analysis_report_generation_node (AnalysisReportGenerationNode): Node for generating reports.
        visualization_action_planing_node (VisualizationActionPlaningNode): Node for planning visualization actions.
        visualization_code_generation_node (VisualizationCodeGenerationNode): Node for generating visualization code.
        code_debagging_node (CodeDebuggingNode): Node for debugging code.
        _graph (StateGraph): Private attribute storing the execution graph instance.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    state: Type[BaseModel]
    task_routing_node: TaskRoutingNode
    task_decomposition_node: TaskDecompositionNode
    task_decomposition_summarization_node: TaskDecompositionSummarizationNode
    subtask_classification_node: SubtaskClassificationNode
    direct_responding_node: DirectRespondingNode
    context_advising_node: ContextAdvisingNode
    analysis_action_planing_node: AnalysisActionPlaningNode
    analysis_code_generation_node: AnalysisCodeGenerationNode
    analysis_report_generation_node: AnalysisReportGenerationNode
    visualization_action_planing_node: VisualizationActionPlaningNode
    visualization_code_generation_node: VisualizationCodeGenerationNode
    code_debagging_node: CodeDebuggingNode

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
        Add all agent workflow nodes to the state graph.

        This includes routing, decomposition, classification, action planning,
        code generation, execution, debugging, reporting, visualization, and memory nodes.
        """
        self._graph.add_node("task_router", self.task_routing_node.invoke)
        self._graph.add_node("task_decomposer", self.task_decomposition_node.invoke)
        self._graph.add_node(
            "task_decomposition_summarizer",
            self.task_decomposition_summarization_node.invoke,
        )
        self._graph.add_node(
            "subtask_classifier", self.subtask_classification_node.invoke
        )
        self._graph.add_node("context_advisor", self.context_advising_node.invoke)

        self._graph.add_node(
            "analysis_action_planner", self.analysis_action_planing_node.invoke
        )
        self._graph.add_node(
            "visualization_action_planner",
            self.visualization_action_planing_node.invoke,
        )

        self._graph.add_node(
            "analysis_code_generator", self.analysis_code_generation_node.invoke
        )
        self._graph.add_node(
            "visualization_code_generator",
            self.visualization_code_generation_node.invoke,
        )
        self._graph.add_node("code_executor", CodeExecutionNode.invoke)
        self._graph.add_node("code_debugger", self.code_debagging_node.invoke)
        self._graph.add_node(
            "analysis_report_generator", self.analysis_report_generation_node.invoke
        )
        self._graph.add_node("visualization_display", VisualizationDisplayNode.invoke)
        self._graph.add_node("direct_responder", self.direct_responding_node.invoke)
        self._graph.add_node("fallback_handler", lambda state: state)
        self._graph.add_node("memory_saver", MemorySaveNode.invoke)

    def _add_edges(self):
        """
        Add static edges between nodes to define execution order.

        These edges are unconditional connections between nodes.
        """
        self._graph.add_edge(START, "task_router")
        self._graph.add_edge("context_advisor", "memory_saver")
        self._graph.add_edge("task_decomposer", "task_decomposition_summarizer")
        self._graph.add_edge("task_decomposition_summarizer", "subtask_classifier")
        self._graph.add_edge("analysis_action_planner", "analysis_code_generator")
        self._graph.add_edge(
            "visualization_action_planner", "visualization_code_generator"
        )
        self._graph.add_edge("analysis_code_generator", "code_executor")
        self._graph.add_edge("visualization_code_generator", "code_executor")
        self._graph.add_edge("code_debugger", "code_executor")
        self._graph.add_edge("fallback_handler", END)
        self._graph.add_edge("memory_saver", END)

    def _add_conditional_edges(self):
        """
        Add conditional edges to the state graph.

        Conditional edges allow the workflow to branch depending on the agent state.
        """
        self._graph.add_conditional_edges(
            "task_router",
            ConditionalRoutingNode.routing_from_task_router,
            {
                "task_decomposer": "task_decomposer",
                "context_advisor": "context_advisor",
            },
        )
        self._graph.add_conditional_edges(
            "subtask_classifier",
            ConditionalRoutingNode.routing_from_subtask_classifier,
            {
                "analysis_action_planner": "analysis_action_planner",
                "visualization_action_planner": "visualization_action_planner",
                "direct_responder": "direct_responder",
            },
        )
        self._graph.add_conditional_edges(
            "code_executor",
            ConditionalRoutingNode.routing_from_code_executor,
            {
                "code_debugger": "code_debugger",
                "fallback_handler": "fallback_handler",
                "analysis_report_generator": "analysis_report_generator",
                "visualization_display": "visualization_display",
            },
        )
        self._graph.add_conditional_edges(
            "analysis_report_generator",
            ConditionalRoutingNode.routing_from_analysis_report_generator,
            {
                "subtask_classifier": "subtask_classifier",
                "memory_saver": "memory_saver",
            },
        )
        self._graph.add_conditional_edges(
            "visualization_display",
            ConditionalRoutingNode.routing_from_visualization_display,
            {
                "subtask_classifier": "subtask_classifier",
                "memory_saver": "memory_saver",
            },
        )
        self._graph.add_conditional_edges(
            "direct_responder",
            ConditionalRoutingNode.routing_from_direct_responder,
            {
                "subtask_classifier": "subtask_classifier",
                "memory_saver": "memory_saver",
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


class AgentGraphRegistry:
    """
    Registry of preconfigured `AgentGraphBuilder` instances for different modes.

    Attributes:
        TECHNICAL_MODE (AgentGraphBuilder): Fully detailed technical workflow.
        QUICK_ANALYSIS_MODE (AgentGraphBuilder): Optimized workflow for fast analysis.
    """

    # TECHNICAL_MODE configuration:
    # Fully-featured agent workflow for in-depth, technical execution.
    # Includes all nodes optimized for detailed task decomposition, analysis,
    # visualization, code generation, debugging, and context-aware advisory.
    TECHNICAL_MODE: Any = AgentGraphBuilder(
        state=AgentState,
        task_routing_node=TaskRoutingNodeRegistry.UNIFIED,
        task_decomposition_node=TaskDecompositionNodeRegistry.TECHNICAL_MODE,
        task_decomposition_summarization_node=TaskDecompositionSummarizationNodeRegistry.TECHNICAL_MODE,
        subtask_classification_node=SubtaskClassificationNodeRegistry.UNIFIED,
        direct_responding_node=DirectRespondingNodeRegistry.TECHNICAL_MODE,
        context_advising_node=ContextAdvisingNodeRegistry.TECHNICAL_MODE,
        analysis_action_planing_node=AnalysisActionPlaningNodeRegistry.TECHNICAL_MODE,
        analysis_code_generation_node=AnalysisCodeGenerationNodeRegistry.TECHNICAL_MODE,
        analysis_report_generation_node=AnalysisReportGenerationNodeRegistry.TECHNICAL_MODE,
        visualization_action_planing_node=VisualizationActionPlaningNodeRegistry.TECHNICAL_MODE,
        visualization_code_generation_node=VisualizationCodeGenerationNodeRegistry.TECHNICAL_MODE,
        code_debagging_node=CodeDebaggingNodeRegistry.UNIFIED,
    ).build()

    # QUICK_ANALYSIS_MODE configuration:
    # Lightweight agent workflow optimized for fast analysis and quick results.
    # Uses simpler, faster execution paths, with fewer steps in decomposition
    # and code generation, while still supporting basic reporting and visualization.
    QUICK_ANALYSIS_MODE: Any = AgentGraphBuilder(
        state=AgentState,
        task_routing_node=TaskRoutingNodeRegistry.UNIFIED,
        task_decomposition_node=TaskDecompositionNodeRegistry.QUICK_ANALYSIS_MODE,
        task_decomposition_summarization_node=TaskDecompositionSummarizationNodeRegistry.QUICK_ANALYSIS_MODE,
        subtask_classification_node=SubtaskClassificationNodeRegistry.UNIFIED,
        direct_responding_node=DirectRespondingNodeRegistry.QUICK_ANALYSIS_MODE,
        context_advising_node=ContextAdvisingNodeRegistry.QUICK_ANALYSIS_MODE,
        analysis_action_planing_node=AnalysisActionPlaningNodeRegistry.QUICK_ANALYSIS_MODE,
        analysis_code_generation_node=AnalysisCodeGenerationNodeRegistry.QUICK_ANALYSIS_MODE,
        analysis_report_generation_node=AnalysisReportGenerationNodeRegistry.QUICK_ANALYSIS_MODE,
        visualization_action_planing_node=VisualizationActionPlaningNodeRegistry.QUICK_VISUALIZATION_MODE,
        visualization_code_generation_node=VisualizationCodeGenerationNodeRegistry.QUICK_VISUALIZATION_MODE,
        code_debagging_node=CodeDebaggingNodeRegistry.UNIFIED,
    ).build()
