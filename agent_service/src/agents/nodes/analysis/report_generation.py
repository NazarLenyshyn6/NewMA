"""
This module defines the `AnalysisReportGenerationNode` and
`AnalysisReportGenerationNodeRegistry` classes, which are responsible for
generating structured analysis reports within the AI agent system.

Core responsibilities:
    - Format analysis report steps and entries for clear readability.
    - Use a language model to generate a polished, human-readable analysis report.
    - Summarize the generated report and store it in the agent state.
    - Record the generated report in memory for future retrieval.
    - Provide preconfigured node instances for different agent modes
      (technical vs. quick analysis).
"""

from typing import override
from pprint import pformat

from agents.nodes.base import BaseNode
from agents.state import AgentState
from agents.prompts.analysis.report_generation import AnalysisReportGenerationPrompt
from agents.models.anthropic_ import high_temp_model
from agents.nodes.summarization import SummarizationNode
from agents.nodes.memory.retrieval import MemoryRetrievalNode


class AnalysisReportGenerationNode(BaseNode):
    """
    Generates structured analysis reports using a language model.

    This node formats raw analysis report steps, invokes a model to generate a
    readable report, updates the agent's summary, and records the output in memory.

    Attributes:
        _chain: The execution chain integrating the model, prompt,
                        and output handling logic.
    """

    @staticmethod
    def _parse_analysis_report(analysis_report: list) -> str:
        """
        Convert a raw analysis report list into a formatted string.

        Args:
            analysis_report: List of analysis steps, where each step
                                    may be a string or a dictionary.

        Returns:
            str: Formatted, human-readable string of the analysis report.
        """

        lines = []
        for i, entry in enumerate(analysis_report, 1):
            lines.append(f"Step {i}:")
            if isinstance(entry, dict):
                # Format dictionary entries with indentation for readability
                for key, value in entry.items():
                    formatted_value = pformat(value, indent=4, width=80)
                    lines.append(f"  {key}: {formatted_value}")
            else:
                lines.append(f"  {entry}")
            lines.append("")

        return "\n".join(lines)

    @override
    def invoke(self, state: AgentState):
        """
        Generate a human-readable analysis report and update the agent state.

        Args:
            state: The current state of the agent, which includes:
                - question: The user’s original query.
                - analysis_report: Raw analysis report steps.
                - analysis_action_plan: Planned analysis steps.
                - analysis_summary: Existing summary of analysis.

        Returns:
            None: Updates the state with the generated report, summary, and memory.
        """

        print("* AnalysisReportGenerationNode -> ")

        # Format raw analysis report for clarity
        analysis_report = self._parse_analysis_report(state.analysis_report)

        # Generate a polished report using the model chain
        generated_report = self._chain.invoke(
            {
                "question": state.question,
                "analysis_report": analysis_report,
                "analysis_action_plan": state.analysis_action_plan,
            }
        ).content

        # Update agent's analysis summary
        SummarizationNode.analysis_summarization(
            state, generated_report, state.analysis_summary
        )

        # Record the generated report in memory for conversation history
        MemoryRetrievalNode.add_answer(state, generated_report)

        # Remove the completed subtask from the queue
        state.subtasks.popleft()

        return state


class AnalysisReportGenerationNodeRegistry:
    """
    Registry of preconfigured `AnalysisReportGenerationNode` instances.

    Provides nodes specialized for different agent modes:
        - TECHNICAL_MODE: Produces detailed, methodical analysis reports.
        - QUICK_ANALYSIS_MODE: Produces concise, rapid analysis reports.

    Attributes:
        TECHNICAL_MODE: Node for technical reporting.
        QUICK_ANALYSIS_MODE: Node for quick reporting.
    """

    # Node for detailed technical analysis report generation
    TECHNICAL_MODE: AnalysisReportGenerationNode = AnalysisReportGenerationNode(
        model=high_temp_model, prompt=AnalysisReportGenerationPrompt.TECHNICAL_MODE
    )

    # Node for quick and lightweight analysis report generation
    QUICK_ANALYSIS_MODE: AnalysisReportGenerationNode = AnalysisReportGenerationNode(
        model=high_temp_model, prompt=AnalysisReportGenerationPrompt.QUICK_ANALYSIS_MODE
    )
