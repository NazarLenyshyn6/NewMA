"""..."""

from enum import Enum
from agent_core.subtask_selectors.enums.base import BaseSubTask


class ClassificationSubTask(BaseSubTask, Enum):
    """..."""

    # Data preparation
    CATEGORICAL_ENCODING = "categorical_encoding"
    FEATURE_SCALING = "feature_scaling"
    FEATURE_SELECTION = "feature_selection"
    DATA_SPLITTING = "data_splitting"

    # Model training and tuning
    MODEL_SELECTION = "model_selection"
    TRAINING = "training"
    HYPERPARAMETER_TUNING = "hyperparameter_tuning"

    # Model evaluation
    MODEL_EVALUATION = "model_evaluation"
    CROSS_VALIDATION = "cross_validation"
    PERFORMANCE_METRICS = "performance_metrics"
    CONFUSION_MATRIX = "confusion_matrix"

    # Interpretation and deployment
    FEATURE_IMPORTANCE = "feature_importance"
    MODEL_EXPLANATION = "model_explanation"
    MODEL_SERIALIZATION = "model_serialization"
    MONITORING = "monitoring"
