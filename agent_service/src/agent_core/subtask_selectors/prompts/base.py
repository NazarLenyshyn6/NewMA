"""..."""

from typing import List, Dict

from pydantic import BaseModel, ConfigDict
from langchain.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from agent_core.subtask_selectors.enums.base import BaseSubTask


class BaseSubTasksSelectionPromptBuilder(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    system_prompt: str
    subtasks: List[BaseSubTask]
    examples: List[Dict[str, str]]

    def build_subtask_selection_prompt(self) -> ChatPromptTemplate:
        """..."""

        example_prompt = ChatPromptTemplate.from_messages(
            [
                HumanMessagePromptTemplate.from_template("{question}"),
                AIMessagePromptTemplate.from_template("{subtask}"),
            ]
        )

        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=self.examples, example_prompt=example_prompt
        )

        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self.system_prompt),
                few_shot_prompt,
                HumanMessagePromptTemplate.from_template("{question}"),
            ]
        )
