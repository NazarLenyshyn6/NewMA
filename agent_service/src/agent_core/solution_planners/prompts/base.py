"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)


class BaseSolutionPlaningPromptBuilder:
    """..."""

    def __init__(self, system_prompt: str):
        self.system_promt = system_prompt

    def build_solution_planing_prompt(self) -> ChatPromptTemplate:
        """..."""
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self.system_promt),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template(
                    "User question: {question}\n\n"
                    "Based on the above, what should be done next?"
                ),
            ]
        )
