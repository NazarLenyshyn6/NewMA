"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class SolutionPlanningPromptTemplate:
    """..."""

    @staticmethod
    def build(system_prompt: str) -> ChatPromptTemplate:
        """..."""
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    system_prompt + "\n\n"
                    "You are a helpful ML engineer assisting with practical data analysis and modeling tasks. "
                    "Provide clear, step-by-step plans that can be followed to solve ML and data problems efficiently, "
                    "especially on user-uploaded data."
                ),
                HumanMessagePromptTemplate.from_template(
                    "Here is the previous context:\n\n"
                    "{history}\n\n"
                    "Use this information to understand the problem better."
                ),
                HumanMessagePromptTemplate.from_template(
                    "User question:\n{question}\n\n"
                    "Please create a clear, step-by-step plan to address this question. "
                    "Focus on practical, implementable steps. "
                    "Include data handling, analysis, and modeling considerations. "
                    "Keep it concise and easy to follow."
                ),
            ]
        )
