from agent_core.models.registry import anthropic_claude_sonnet_4_20250514_model
from agent_core.solution_planners.planners.base import BaseSolutionPlanner
from agent_core.solution_planners.prompts.classification import (
    CLASSIFICATION_REFLECTION_PROMPTS,
)
from agent_core.solution_planners.memory import solutions_memory_manager
from agent_core.subtask_selectors.enums.classification import ClassificationSubTask


categorical_encoding_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.CATEGORICAL_ENCODING
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas", "sklearn.preprocessing", "category_encoders"],
)

feature_scaling_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.FEATURE_SCALING
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn.preprocessing", "pandas", "numpy"],
)

feature_selection_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.FEATURE_SELECTION
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn.feature_selection", "pandas", "numpy"],
)

data_splitting_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.DATA_SPLITTING
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn.model_selection", "pandas", "numpy"],
)

model_selection_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.MODEL_SELECTION
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn", "xgboost", "lightgbm", "catboost"],
)

training_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[ClassificationSubTask.TRAINING],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn", "xgboost", "lightgbm", "catboost", "torch", "tensorflow"],
)

hyperparameter_tuning_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.HYPERPARAMETER_TUNING
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn.model_selection", "optuna", "ray.tune", "hyperopt"],
)

model_evaluation_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.MODEL_EVALUATION
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn.metrics", "matplotlib", "seaborn", "pandas"],
)

cross_validation_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.CROSS_VALIDATION
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn.model_selection", "pandas", "numpy"],
)

performance_metrics_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.PERFORMANCE_METRICS
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn.metrics", "matplotlib", "seaborn", "pandas"],
)

confusion_matrix_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.CONFUSION_MATRIX
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["sklearn.metrics", "matplotlib", "seaborn"],
)

feature_importance_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.FEATURE_IMPORTANCE
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["shap", "sklearn", "xgboost", "lightgbm", "catboost", "pandas"],
)

model_explanation_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.MODEL_EXPLANATION
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["shap", "lime", "sklearn", "pandas", "matplotlib"],
)

model_serialization_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[
        ClassificationSubTask.MODEL_SERIALIZATION
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["joblib", "pickle", "sklearn"],
)

monitoring_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=CLASSIFICATION_REFLECTION_PROMPTS[ClassificationSubTask.MONITORING],
    memory_manager=solutions_memory_manager,
    dependencies=["prometheus_client", "scikit-multiflow", "pandas", "numpy"],
)
