"""..."""

from agent.template.classifiers.tasks import TasksClassificationPromptTemplate
from agent.enums.classifiers.tasks import Tasks
from agent.examples.classifiers.tasks import tasks_classification_examples

tasks_classification_prompt = TasksClassificationPromptTemplate.build(
    tasks=list(Tasks), examples=tasks_classification_examples
)
