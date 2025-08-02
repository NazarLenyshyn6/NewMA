"""..."""

from typing import List, Dict

from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
)


class SubTasksClassificationPromptTemplate:
    """..."""

    @staticmethod
    def build(
        system_prompt: str, subtasks: List, examples: List[Dict[str, str]]
    ) -> ChatPromptTemplate:
        """..."""
        example_prompt = ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate.from_template("{question}"),
                AIMessagePromptTemplate.from_template("{subtask}"),
            ],
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=examples, example_prompt=example_prompt
        )

        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                few_shot_prompt,
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
