"""..."""

from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.registry.memory.planners import solution_planner_memory_manager
from agent.planners import SolutionPlanner
from agent.prompts.planners import eda


missing_values_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.missing_values_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["numpy", "pandas"],
)

duplicate_rows_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.duplicate_rows_detection_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

data_types_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.data_types_check_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

unique_values_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.unique_values_analysis_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

statistical_summary_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.statistical_summary_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "scipy"],
)

distribution_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.distribution_analysis_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "scipy", "numpy"],
)

outlier_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.outliers_detection_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["numpy", "scipy", "pandas"],
)

correlation_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.correlation_analysis_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "seaborn", "matplotlib"],
)

pair_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.pair_plots_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "matplotlib", "pandas"],
)

categorical_vs_target_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.categorical_vs_target_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "pandas", "matplotlib"],
)

numerical_vs_target_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.numerical_vs_target_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas", "numpy"],
)

missing_value_imputation_strategy_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.missing_value_imputation_stragety_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "sklearn.impute", "numpy"],
)

class_distribution_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.class_distribution_check_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "matplotlib", "seaborn", "imbalanced-learn", "imblearn"],
)

heatmaps_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.heatmaps_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "matplotlib", "numpy", "pandas"],
)

time_series_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.time_series_analysis_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "statsmodels", "matplotlib"],
)

data_provenance_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.data_provenance_check_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

log_transformation_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.log_transformation_check_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["numpy", "pandas", "matplotlib"],
)

data_completeness_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.data_completeness_check_solution_planning_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)
