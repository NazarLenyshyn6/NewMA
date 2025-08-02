"""..."""

from typing import Any, List

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage


class SubtasksClassifier(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate
    subtasks: List

    _subtasks_classification_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._subtasks_classification_chain = (
            self.prompt
            | self.model
            | RunnableLambda(lambda subtasks: self._parse_subtasks(subtasks))
        )

    @staticmethod
    def _parse_subtasks(subtasks: AIMessage) -> List[str]:
        """..."""
        return [subtask.strip() for subtask in subtasks.content.split(",")]

    def classify(self, question: str) -> List[str]:
        """..."""
        tasks = self._subtasks_classification_chain.invoke(
            {
                "question": question,
                "subtasks": ", ".join(subtask.name for subtask in self.subtasks),
            }
        )
        return tasks
