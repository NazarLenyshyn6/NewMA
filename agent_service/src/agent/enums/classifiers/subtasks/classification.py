"""..."""

from enum import Enum, auto


class ClassificationSubTasks(Enum):
    """..."""

    CATEGORICAL_ENCODING = auto()
    FEATURE_SCALING = auto()
    FEATURE_SELECTION = auto()
    DATA_SPLITTING = auto()
    MODEL_SELECTION = auto()
    TRAINING = auto()
    HYPERPARAMETER_TUNING = auto()
    MODEL_EVALUATION = auto()
    CROSS_VALIDATION = auto()
    PERFORMANCE_METRICS = auto()
    CONFUSION_MATRIX = auto()
    FEATURE_IMPORTANCE = auto()
    MODEL_EXPLANATION = auto()
    MODEL_SERIALIZATION = auto()
    MONITORING = auto()
