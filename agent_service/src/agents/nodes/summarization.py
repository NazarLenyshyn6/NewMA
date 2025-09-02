"""
Summarization Node Module.

This module defines the `SummarizationNode` class, which provides
static helper methods to perform summarization of different agent
content types (analysis reports, visualization plans, code, and
user preferences) using a low-temperature Anthropic model.

The node updates the `AgentState` with the generated summaries,
ensuring a consistent interface for all summarization operations.
"""

from typing import Dict

from agents.models.anthropic_ import low_temp_model
from agents.state import AgentState
from agents.prompts.summarization import SummarizationPrompt


class SummarizationNode:
    """
    Node for generating content summaries using a low-temperature LLM.

    `SummarizationNode` provides static methods that take agent data
    (analysis reports, visualization plans, code, user preferences)
    and produce condensed summaries, which are stored in the
    `AgentState`.

    All methods are static since summarization does not depend on
    instance-specific state and can operate solely on the inputs
    provided and the agent state.
    """

    @staticmethod
    def analysis_summarization(
        state: AgentState, analysis_report: str, analysis_summary: str
    ):
        """
        Summarize the agent's analysis report and update the agent state.

        Args:
            state: The current agent execution state.
            analysis_report: The detailed analysis report text.
            analysis_summary: Previous or partial summary for context.

        Updates:
            state.analysis_summary: The newly generated analysis summary.
        """
        print("* AnalysisSummarizationNode -> ")
        chain = SummarizationPrompt.ANALYSIS | low_temp_model
        state.analysis_summary = chain.invoke(
            {"analysis_report": analysis_report, "analysis_summary": analysis_summary},
            config={"metadata": {"stream": False}},
        ).content

    @staticmethod
    def visualization_summarization(
        state: AgentState, visualization_plan: str, visualization_summary: str
    ):
        """
        Summarize the agent's visualization plan and update the agent state.

        Args:
            state: The current agent execution state.
            visualization_plan: The detailed visualization plan text.
            visualization_summary: Previous or partial summary for context.

        Updates:
            state.visualization_summary: The newly generated visualization summary.
        """
        print("* VisualizationSummarizationNode -> ")
        chain = SummarizationPrompt.VISUALIZATION | low_temp_model
        state.visualization_summary = chain.invoke(
            {
                "visualization_plan": visualization_plan,
                "visualization_summary": visualization_summary,
            },
            config={"metadata": {"stream": False}},
        ).content

    @staticmethod
    def code_summarization(
        state: AgentState, code: str, code_summary: str, variables: Dict
    ):
        """
        Summarize the agent's code and related variables, updating the agent state.

        Args:
            state: The current agent execution state.
            code: The source code to summarize.
            code_summary: Previous or partial code summary for context.
            variables (Dict): Current variable states that may influence the summary.

        Updates:
            state.code_summary: The newly generated code summary.
        """
        print("* CodeSummarizationNode -> ")
        chain = SummarizationPrompt.CODE | low_temp_model
        state.code_summary = chain.invoke(
            {"code": code, "code_summary": code_summary, "variables": variables.keys()},
            config={"metadata": {"stream": False}},
        ).content

    @staticmethod
    def user_preferences_summarization(
        state: AgentState, question: str, user_preferences_summary: str
    ):
        """
        Summarize user preferences based on a question, updating the agent state.

        Args:
            state: The current agent execution state.
            question: The current user query or context.
            user_preferences_summary: Previous or partial user preference summary.

        Updates:
            state.user_preferences_summary: The newly generated user preferences summary.
        """
        print("* UserPreferencesSummarizationNode -> ")
        chain = SummarizationPrompt.USER_PREFERENCES | low_temp_model
        state.user_preferences_summary = chain.invoke(
            {
                "question": question,
                "user_preferences_summary": user_preferences_summary,
            },
            config={"metadata": {"stream": False}},
        ).content

    @staticmethod
    def pending_context_summarization(
        state: AgentState, question: str, context: str, pending_context: str
    ):
        """
        Summarize the pending context based on the current question and agent state.

        Args:
            state: The current agent execution state.
            question: The current user query.
            context: The current context of the agent’s execution.
            pending_context: Previous pending context awaiting confirmation or execution.

        Updates:
            state.pending_context: The newly generated, condensed pending context summary.
        """
        print("* PendingContextSummarizationNode -> ")
        chain = SummarizationPrompt.PENDING_CONTEXT | low_temp_model
        state.pending_context = chain.invoke(
            {
                "question": state.question,
                "context": context,
                "pending_context": state.pending_context,
            },
            config={"metadata": {"stream": False}},
        ).content
