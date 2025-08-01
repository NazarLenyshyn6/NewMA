"""..."""

from typing import Any, List, Dict, Union

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


class SubTaskSelector(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    subtask_prompt_templates: Dict[Task, ChatPromptTemplate]
    avaliable_subtasks: Dict[Task, List[BaseSubTask]]

    _subtasks_detection_chain: Runnable = PrivateAttr()
    _task_specific_runnables: Dict[Task, Runnable] = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._task_specific_runnables = self._build_task_chains()
        self._subtasks_detection_chain = (
            RunnableLambda(lambda input: self._prepare_prompt_input(input))
            | RunnableLambda(lambda input: self._run_task_prompt_chain(input))
            | RunnableLambda(
                lambda subtasks_str: self._parse_subtask_list_string(subtasks_str)
            )
        )

    def _build_task_chains(self) -> Dict[Task, Runnable]:
        """..."""
        chains = {}
        for task, _ in self.avaliable_subtasks.items():
            prompt_template = self.subtask_prompt_templates.get(task)
            if prompt_template is None:
                raise KeyError(f"Missing prompt template for task: {task}")
            chains[task] = prompt_template | self.model
        return chains

    def _prepare_prompt_input(
        self, input: Dict[str, str]
    ) -> Dict[str, Union[str, List[BaseSubTask]]]:
        """..."""
        question = input.get("question")
        task_str = input.get("task")
        if question is None or task_str is None:
            KeyError("Input must inclue 'question' and 'task' keys.")
        task_enum = Task.from_string(task_str)
        subtasks = self.avaliable_subtasks.get(task_enum)
        if subtasks is None:
            raise KeyError(f"No subtasks defined for task: {task_str}")
        return {"question": question, "subtasks": subtasks, "task": task_str}

    def _run_task_prompt_chain(
        self, input: Dict[str, Union[str, List[BaseSubTask]]]
    ) -> str:
        """..."""
        task = input.get("task")
        task_chain = self._task_specific_runnables.get(task)
        if task_chain is None:
            raise KeyError(f"No runnable chain found for task: {task}")
        input.pop("task")
        return task_chain.invoke(input=input).content

    @staticmethod
    def _parse_subtask_list_string(subtasks_str: str) -> List[str]:
        """..."""
        return [subtask.strip() for subtask in subtasks_str.split(",")]

    def select(self, question: str, tasks: List[str]) -> List[str]:
        """..."""
        inputs = [{"question": question, "task": task} for task in tasks]
        subtasks_per_task = self._subtasks_detection_chain.batch(inputs=inputs)
        return [task for subtasks in subtasks_per_task for task in subtasks]


subtask_prompt_templates = {
    Task.EDA: eda_subtasks_selection_prompt_builder.build_subtask_selection_prompt(),
    Task.CLASSIFICATION: classification_subtasks_selection_prompt_builder.build_subtask_selection_prompt(),
}
avaliable_subtasks = {
    Task.EDA: list(EdaSubTask),
    Task.CLASSIFICATION: list(ClassificationSubTask),
}

sub_task_selector = SubTaskSelector(
    model=anthropic_claude_sonnet_4_20250514_model,
    subtask_prompt_templates=subtask_prompt_templates,
    avaliable_subtasks=avaliable_subtasks,
)

# combined_eda_classification_questions = [
#     {
#         "question": "I want to predict whether users will subscribe — what should I check in the data first?",
#         "desired_output": {
#             "EDA": [
#                 "Missing Value Detection",
#                 "Feature Type Detection",
#                 "Data Distribution",
#             ],
#             "CLASSIFICATION": ["Task Type Inference", "Model Selection"],
#         },
#     },
#     {
#         "question": "Can you help me prepare the dataset and pick the right classifier?",
#         "desired_output": {
#             "EDA": [
#                 "Missing Value Detection",
#                 "Categorical Summary",
#                 "Feature Scaling Decision",
#             ],
#             "CLASSIFICATION": ["Model Selection"],
#         },
#     },
#     {
#         "question": "What should I do before building a churn prediction model?",
#         "desired_output": {
#             "EDA": [
#                 "Outlier Detection",
#                 "Missing Value Detection",
#                 "Feature Type Detection",
#             ],
#             "CLASSIFICATION": ["Model Selection", "Class Imbalance Detection"],
#         },
#     },
#     {
#         "question": "Which columns are useful for predicting customer satisfaction?",
#         "desired_output": {
#             "EDA": ["Feature Type Detection", "Correlation Analysis"],
#             "CLASSIFICATION": ["Feature Importance Analysis"],
#         },
#     },
#     {
#         "question": "What preprocessing is required to train a model on this dataset?",
#         "desired_output": {
#             "EDA": [
#                 "Missing Value Detection",
#                 "Categorical Summary",
#                 "Feature Type Detection",
#             ],
#             "CLASSIFICATION": [
#                 "Categorical Encoding Strategy",
#                 "Feature Scaling Decision",
#             ],
#         },
#     },
#     {
#         "question": "How can I explore the target variable and then train a model on it?",
#         "desired_output": {
#             "EDA": ["Target Distribution", "Descriptive Statistics"],
#             "CLASSIFICATION": ["Class Distribution Analysis", "Model Selection"],
#         },
#     },
#     {
#         "question": "I’m getting low accuracy — is there something wrong with my features?",
#         "desired_output": {
#             "EDA": ["Correlation Analysis", "Outlier Detection"],
#             "CLASSIFICATION": ["Feature Importance Analysis", "Model Evaluation"],
#         },
#     },
#     {
#         "question": "How do I detect problems in the dataset before running classification?",
#         "desired_output": {
#             "EDA": [
#                 "Missing Value Detection",
#                 "Outlier Detection",
#                 "Data Distribution",
#             ],
#             "CLASSIFICATION": ["Class Imbalance Detection"],
#         },
#     },
#     {
#         "question": "Can you walk me through building a classifier for imbalanced classes?",
#         "desired_output": {
#             "EDA": ["Class Distribution Analysis", "Target Distribution"],
#             "CLASSIFICATION": ["Class Imbalance Strategy", "Model Selection"],
#         },
#     },
#     {
#         "question": "What should I analyze in the data before choosing the best classifier?",
#         "desired_output": {
#             "EDA": [
#                 "Feature Type Detection",
#                 "Data Distribution",
#                 "Missing Value Detection",
#             ],
#             "CLASSIFICATION": ["Model Selection"],
#         },
#     },
#     {
#         "question": "I'm training a classification model — should I explore feature distributions first?",
#         "desired_output": {
#             "EDA": ["Data Distribution", "Feature Type Detection"],
#             "CLASSIFICATION": ["Feature Importance Analysis"],
#         },
#     },
#     {
#         "question": "Before evaluating my model, how can I explore the class labels and errors?",
#         "desired_output": {
#             "EDA": ["Target Distribution", "Outlier Detection"],
#             "CLASSIFICATION": ["Model Evaluation", "Confusion Matrix Analysis"],
#         },
#     },
#     {
#         "question": "How do I clean the data and build a robust classifier?",
#         "desired_output": {
#             "EDA": ["Missing Value Detection", "Outlier Detection"],
#             "CLASSIFICATION": ["Model Selection", "Hyperparameter Tuning Strategy"],
#         },
#     },
#     {
#         "question": "Which features and classes should I inspect before modeling?",
#         "desired_output": {
#             "EDA": ["Categorical Summary", "Feature Type Detection"],
#             "CLASSIFICATION": [
#                 "Class Distribution Analysis",
#                 "Feature Importance Analysis",
#             ],
#         },
#     },
#     {
#         "question": "Can you help me go from raw data to a trained classification model?",
#         "desired_output": {
#             "EDA": [
#                 "Missing Value Detection",
#                 "Feature Type Detection",
#                 "Data Distribution",
#             ],
#             "CLASSIFICATION": ["Model Selection", "Categorical Encoding Strategy"],
#         },
#     },
# ]

# from agent_core.task_selectors.builder import task_selector

# for sample in combined_eda_classification_questions:
#     question = sample["question"]
#     output = sample["desired_output"]
#     tasks = task_selector.select(question)
#     print(f"{question}: {sub_task_selector.select(question=question, tasks=tasks)}")
