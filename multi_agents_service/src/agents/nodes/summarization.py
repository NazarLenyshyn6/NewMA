"""..."""

from typing import Dict

from agents.prompts.summarization.code import code_summarization_prompt
from agents.prompts.summarization.conversation import conversation_summarization_prompt
from agents.models.anthropic_ import summarization_model


class SummarizationNode:

    @staticmethod
    def code_summarization(code: str, code_memory: str, variables_memory: Dict):
        """..."""
        print("* SummarizationNode -> ")
        code_summarization_chain = code_summarization_prompt | summarization_model
        return code_summarization_chain.invoke(
            {
                "code": code,
                "history": code_memory,
                "variables_memory": variables_memory.keys(),
            },
            config={"metadata": {"stream": False}},
        ).content

    @staticmethod
    def conversation_summarization(conversation_summary_memory: str, report: str):
        """..."""
        conversation_summarization_chain = (
            conversation_summarization_prompt | summarization_model
        )
        return conversation_summarization_chain.invoke(
            {
                "conversation": report,
                "history": conversation_summary_memory,
            },
            config={"metadata": {"stream": False}},
        ).content
