"""..."""

from typing import Dict, List, Any

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable, RunnableLambda


from agent.classifiers.subtasks import SubtasksClassifier


class SubTasksClassificationRunner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    classifiers: Dict[str, SubtasksClassifier]

    _subtasks_classification_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._subtasks_classification_chain = RunnableLambda(
            lambda input: self._get_classifier(input)
        ) | RunnableLambda(lambda input: self._classify(input))

    def _get_classifier(self, input: Dict) -> Dict:
        """..."""
        task = input.get("task")
        classifier = self.classifiers.get(task)
        if classifier is None:
            raise
        input["classifier"] = classifier
        input.pop("task")
        return input

    def _classify(self, input: Dict) -> str:
        classifier: Runnable = input.get("classifier")
        question: SubtasksClassifier = input.get("question")
        return classifier.classify(question)

    def classify(self, qeustion: str, tasks: List[str]) -> List[str]:
        """..."""
        inputs = [{"question": qeustion, "task": task} for task in tasks]
        subtasks_per_task = self._subtasks_classification_chain.batch(inputs)
        return [task for subtasks in subtasks_per_task for task in subtasks]
