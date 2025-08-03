"""..."""

from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.registry.memory.planners import solution_planner_memory_manager
from agent.planners import SolutionPlanner
from agent.prompts.planners import classification


categorical_encoding_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.categorical_encoding_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "sklearn.preprocessing", "category_encoders"],
)

feature_scaling_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.feature_scaling_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn.preprocessing", "pandas", "numpy"],
)


data_splitting_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.data_splitting_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn.model_selection", "pandas", "numpy"],
)

model_selection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.model_selection_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "xgboost", "lightgbm", "catboost"],
)

training_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.training_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "xgboost", "lightgbm", "catboost", "torch", "tensorflow"],
)

hyperparameter_tuning_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.hyperparameter_tuning_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn.model_selection", "optuna", "ray.tune", "hyperopt"],
)

model_evaluation_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.model_evaluation_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn.metrics", "matplotlib", "seaborn", "pandas"],
)

cross_validation_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.cross_validation_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn.model_selection", "pandas", "numpy"],
)

performance_metrics_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.performance_metrics_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn.metrics", "matplotlib", "seaborn", "pandas"],
)

confusion_matrix_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.confusion_matrix_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn.metrics", "matplotlib", "seaborn"],
)

feature_importance_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.feature_importance_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["shap", "sklearn", "xgboost", "lightgbm", "catboost", "pandas"],
)

model_explanation_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.model_explanation_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["shap", "lime", "sklearn", "pandas", "matplotlib"],
)

model_serialization_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.model_serialization_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["joblib", "pickle", "sklearn"],
)

monitoring_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=classification.monitoring_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["prometheus_client", "scikit-multiflow", "pandas", "numpy"],
)
