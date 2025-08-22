"""..."""

from pprint import pformat

from langchain.schema import AIMessage
from langchain.schema.runnable import RunnableLambda

from agents.nodes.base import BaseNode
from agents.prompts.reporting.expert import expert_reporting_prompt
from agents.models.anthropic_ import expert_reporting_model, lambda_model
from agents.state import AgentState
from agents.nodes.summarization import SummarizationNode


class ReportingNode(BaseNode):

    @staticmethod
    def _parse_analysis_report(analysis_report: list) -> str:
        """..."""

        lines = []
        for i, entry in enumerate(analysis_report, 1):
            lines.append(f"Step {i}:")
            if isinstance(entry, dict):
                for key, value in entry.items():
                    formatted_value = pformat(value, indent=4, width=80)
                    lines.append(f"  {key}: {formatted_value}")
            else:
                lines.append(f"  {entry}")
            lines.append("")

        return "\n".join(lines)

    def report(self, state: AgentState) -> AgentState:
        print("* ReportingNodes -> ")
        if state.code_mode == "CODE":
            analysis_report = self._parse_analysis_report(state.analysis_report)
            report = self._chain.invoke(
                {
                    "question": state.question,
                    "report": analysis_report,
                    "execution_plan": state.execution_plan,
                }
            ).content

            # Update conversation summary memory
            state.conversation_summary_memory = (
                SummarizationNode.conversation_summarization(
                    conversation_summary_memory=state.conversation_summary_memory,
                    report=report,
                )
            )

            # Add report to conversation memory
            state.conversation_memory[0]["answer"] = (
                state.conversation_memory[0]["answer"] + report
            )

        else:
            # Placehodler llm call go yield endoded image to frontend with requied metadata
            image_streaming_model = RunnableLambda(
                lambda _: AIMessage(
                    content=state.image, additional_kwargs={}, response_metadata={}
                )
            )
            image_streaming_model.invoke("...", config={"metadata": {"image": True}})

        # Remove subtask
        state.subtasks.popleft()
        return state


expert_reporting_node = ReportingNode(
    model=expert_reporting_model, prompt=expert_reporting_prompt
)
