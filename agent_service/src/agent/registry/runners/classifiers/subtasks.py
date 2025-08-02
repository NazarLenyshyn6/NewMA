"""..."""

from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.runners.classifiers.subtasks import SubTasksClassificationRunner
from agent.enums.classifiers.tasks import Tasks
from agent.registry.classifiers.subtasks import (
    eda_subtasks_classifier,
    classification_subtasks_classifier,
)

classifiers = {
    Tasks.EDA.name: eda_subtasks_classifier,
    Tasks.CLASSIFICATION.name: classification_subtasks_classifier,
}

subtasks_classification_runner = SubTasksClassificationRunner(
    model=anthropic_claude_sonnet_4_20250514_model, classifiers=classifiers
)
