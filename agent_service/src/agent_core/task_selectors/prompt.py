"""..."""

from typing import List, Dict

from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from agent_core.task_selectors.enums import Task


class TaskSelectionPromptBuilder:
    """..."""

    @staticmethod
    def build_task_selection_prompt(
        tasks: List[Task], examples: List[Dict[str, str]]
    ) -> ChatPromptTemplate:
        """..."""

        example_prompt = ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate.from_template("{question}"),
                AIMessagePromptTemplate.from_template("{task}"),
            ]
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=examples, example_prompt=example_prompt
        )

        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    """You are a professional data scientist.
                    Your task is to classify the user's question into one or more of the following machine learning categories: {tasks}.
                    Only include tasks that are clearly required by the question.
                    If the user's question is not about machine learning or data analysis, label it as 'OTHER'.
                    
                    You must:
                    - Be strict in classifying non-ML questions as 'OTHER'
                    - Never attempt to invent an ML task for unrelated topics
                    - Respond ONLY with a comma-separated list of task names from: {tasks}
                    - Do NOT explain or add commentary

                    Answer concisely."""
                ),
                few_shot_prompt,
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
