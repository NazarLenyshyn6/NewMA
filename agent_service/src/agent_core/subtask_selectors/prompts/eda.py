"""..."""

from agent_core.subtask_selectors.prompts.base import BaseSubTasksSelectionPromptBuilder
from agent_core.subtask_selectors.enums.eda import EdaSubTask
from agent_core.subtask_selectors.few_shot_examples.eda import (
    EDA_SUBTASK_SELECTION_EXAMPLES,
)

system_prompt = """You are a professional data scientist, with deep expertise in Exploratory Data Analysis (EDA).
Your task is to classify the user's question into one or more of the following EDA subtasks: {subtasks}.
Only include subtasks that are directly and clearly required to address the user's question.

Strict rules:
- Respond ONLY with a comma-separated list of valid subtask names from the list: {subtasks}
- NEVER invent or guess subtasks not in the list
- If the question is not relevant to EDA, respond ONLY with 'OTHER'
- Do NOT explain, summarize, or comment—respond with only the subtask name(s)

Your answer will be used to route the user query to the appropriate EDA logic chain. Be accurate and precise."""

eda_subtasks_selection_prompt_builder = BaseSubTasksSelectionPromptBuilder(
    system_prompt=system_prompt,
    subtasks=list(EdaSubTask),
    examples=EDA_SUBTASK_SELECTION_EXAMPLES,
)
