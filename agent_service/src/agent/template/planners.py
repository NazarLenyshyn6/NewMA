"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)


class SolutionPlanningPromptTemplate:
    """..."""

    @staticmethod
    def build(system_prompt: str):
        """..."""
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template(
                    "User question: {question}\n\n"
                    "Based on the above, solve user question."
                ),
            ]
        )
