"""..."""

from typing import Any, List

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage


from agent_core.models.registry import anthropic_claude_sonnet_4_20250514_model
from agent_core.task_selectors.enums import Task
from agent_core.task_selectors.prompt import TaskSelectionPromptBuilder
from agent_core.task_selectors.few_shot_examples import TASK_SELECTION_EXAMPLES


class TaskSelector(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    task_prompt_template: ChatPromptTemplate
    avaliable_tasks: List[Task]

    _task_detection_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._task_detection_chain = (
            self.task_prompt_template
            | self.model
            | RunnableLambda(lambda tasks: self._parse_tasks(tasks))
        )

    @staticmethod
    def _parse_tasks(tasks: AIMessage) -> List[str]:
        """..."""
        return [task.strip() for task in tasks.content.split(",")]

    def select(self, question: str) -> List[str]:
        """..."""
        tasks = self._task_detection_chain.invoke(
            {
                "question": question,
                "tasks": ", ".join(t.value for t in self.avaliable_tasks),
            }
        )
        return tasks


task_prompt_template = TaskSelectionPromptBuilder.build_task_selection_prompt(
    tasks=list(Task), examples=TASK_SELECTION_EXAMPLES
)
avaliable_tasks = list(Task)

task_selector = TaskSelector(
    model=anthropic_claude_sonnet_4_20250514_model,
    task_prompt_template=task_prompt_template,
    avaliable_tasks=avaliable_tasks,
)
