"""..."""

from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.classifiers.subtasks import SubtasksClassifier
from agent.prompts.classifiers.subtasks.eda import eda_subtasks_classification_prompt
from agent.prompts.classifiers.subtasks.classification import (
    classification_subtasks_classification_prompt,
)
from agent.enums.classifiers.subtasks.eda import EdaSubTasks
from agent.enums.classifiers.subtasks.classification import ClassificationSubTasks

eda_subtasks_classifier = SubtasksClassifier(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda_subtasks_classification_prompt,
    subtasks=list(EdaSubTasks),
)


classification_subtasks_classifier = SubtasksClassifier(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification_subtasks_classification_prompt,
    subtasks=list(ClassificationSubTasks),
)
