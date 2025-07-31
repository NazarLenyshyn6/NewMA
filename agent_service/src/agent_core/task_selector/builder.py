"""..."""

from typing import Any, List

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate


from agent_core.models.registry import anthropic_claude_sonnet_4_20250514_model
from agent_core.task_selector.enums import Task
from agent_core.task_selector.prompt import TaskSelectionPromptBuilder
from agent_core.task_selector.few_shot_examples import TASK_SELECTION_EXAMPLES


class TaskSelector(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate
    tasks: List[Task]

    _chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._chain = self.prompt | self.model

    @staticmethod
    def _parse_output(tasks: str) -> List[Task]:
        """..."""
        parsed = []
        for task in tasks.split(", "):
            parsed.append(task)
        return parsed

    def select(self, question: str) -> List[Task]:
        """..."""
        tasks = self._chain.invoke(
            {"question": question, "tasks": ", ".join(t.value for t in self.tasks)}
        ).content
        return self._parse_output(tasks)


prompt = TaskSelectionPromptBuilder.build_task_selection_prompt(
    tasks=list(Task), examples=TASK_SELECTION_EXAMPLES
)

task_selector = TaskSelector(
    model=anthropic_claude_sonnet_4_20250514_model, prompt=prompt, tasks=list(Task)
)
