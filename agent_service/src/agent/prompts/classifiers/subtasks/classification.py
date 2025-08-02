"""..."""

from agent.template.classifiers.subtasks import SubTasksClassificationPromptTemplate
from agent.enums.classifiers.subtasks.classification import ClassificationSubTasks
from agent.examples.classifiers.subtasks.classification import (
    classification_subtasks_classification_examples,
)

system_prompt = """You are a professional data scientist with deep expertise in end-to-end classification workflows.

Your task is to classify the user's question into one or more of the following classification subtasks: {subtasks}.
These subtasks represent the full lifecycle of a classification project.

Strict rules:
- Respond ONLY with a comma-separated list of valid subtask names from the list: {subtasks}
- NEVER invent or guess subtasks not in the list
- If the question is not relevant to classification, select the most relevant.
- Do NOT explain, summarize, or comment—respond with only the subtask name(s)

Your answer will be used to route the user query to the appropriate classification logic."""

classification_subtasks_classification_prompt = (
    SubTasksClassificationPromptTemplate.build(
        system_prompt=system_prompt,
        subtasks=list(ClassificationSubTasks),
        examples=classification_subtasks_classification_examples,
    )
)
