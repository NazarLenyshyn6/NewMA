"""..."""

from typing import Any, List

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage


from agent.enums.classifiers.tasks import Tasks


class TasksClassificationRunner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate
    tasks: List[Tasks]

    _tasks_classification_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._tasks_classification_chain = (
            self.prompt
            | self.model
            | RunnableLambda(lambda tasks: self._parse_tasks(tasks))
        )

    @staticmethod
    def _parse_tasks(tasks: AIMessage) -> List[str]:
        """..."""
        return [task.strip() for task in tasks.content.split(",")]

    def classify(self, question: str) -> List[str]:
        """..."""
        tasks = self._tasks_classification_chain.invoke(
            {
                "question": question,
                "tasks": ", ".join(task.name for task in self.tasks),
            }
        )
        return tasks
