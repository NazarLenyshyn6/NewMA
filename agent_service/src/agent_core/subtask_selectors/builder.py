"""..."""

from typing import Any, List, Dict

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.prompts import ChatPromptTemplate


from agent_core.models.registry import anthropic_claude_sonnet_4_20250514_model
from agent_core.task_selectors.enums import Task
from agent_core.subtask_selectors.enums.base import BaseSubTask
from agent_core.subtask_selectors.enums.eda import EdaSubTask
from agent_core.subtask_selectors.enums.classification import ClassificationSubTask
from agent_core.subtask_selectors.prompts.eda import (
    eda_subtasks_selection_prompt_builder,
)
from agent_core.subtask_selectors.prompts.classification import (
    classification_subtasks_selection_prompt_builder,
)
from agent_core.subtask_selectors.prompts.base import BaseSubTasksSelectionPromptBuilder


class SubTaskSelector(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompts: Dict[Task, ChatPromptTemplate]
    subtasks: Dict[Task, List[BaseSubTask]]

    _chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._chain = self.model

    def select(self, question: str, tasks: List[str]) -> List[List[str]]:
        """..."""
        ...


prompts = {
    Task.EDA: eda_subtasks_selection_prompt_builder.build_subtask_selection_prompt(),
    Task.CLASSIFICATION: classification_subtasks_selection_prompt_builder.build_subtask_selection_prompt(),
}
subtasks = {
    Task.EDA: list(EdaSubTask),
    Task.CLASSIFICATION: list(ClassificationSubTask),
}

sub_task_selector = SubTaskSelector(
    model=anthropic_claude_sonnet_4_20250514_model, prompts=prompts, subtasks=subtasks
)
