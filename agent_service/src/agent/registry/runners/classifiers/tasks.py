"""..."""

from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.runners.classifiers.tasks import TasksClassificationRunner
from agent.prompts.classifiers.tasks import tasks_classification_prompt
from agent.enums.classifiers.tasks import Tasks


tasks_classification_runner = TasksClassificationRunner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=tasks_classification_prompt,
    tasks=list(Tasks),
)
