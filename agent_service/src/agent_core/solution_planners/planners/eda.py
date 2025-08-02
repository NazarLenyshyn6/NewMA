from agent_core.models.registry import anthropic_claude_sonnet_4_20250514_model
from agent_core.solution_planners.planners.base import BaseSolutionPlanner
from agent_core.solution_planners.prompts.eda import EDA_REFLECTION_PROMPTS
from agent_core.solution_planners.memory import solutions_memory_manager
from agent_core.subtask_selectors.enums.eda import EdaSubTask


missing_values_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.MISSING_VALUES],
    memory_manager=solutions_memory_manager,
    dependencies=["numpy", "pandas"],
)

duplicate_rows_detection_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.DUPLICATE_ROWS_DETECTION],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas"],
)

data_types_check_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.DATA_TYPES_CHECK],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas", "numpy"],
)

unique_values_analysis_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.UNIQUE_VALUES_ANALYSIS],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas"],
)

statistical_summary_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.STATISTICAL_SUMMARY],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas", "numpy", "scipy"],
)

distribution_analysis_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.DISTRIBUTION_ANALYSIS],
    memory_manager=solutions_memory_manager,
    dependencies=["matplotlib", "seaborn", "scipy", "numpy"],
)

outlier_detection_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.OUTLIER_DETECTION],
    memory_manager=solutions_memory_manager,
    dependencies=["numpy", "scipy", "pandas"],
)

correlation_analysis_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.CORRELATION_ANALYSIS],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas", "numpy", "seaborn", "matplotlib"],
)

pair_plots_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.PAIR_PLOTS],
    memory_manager=solutions_memory_manager,
    dependencies=["seaborn", "matplotlib", "pandas"],
)

categorical_vs_target_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.CATEGORICAL_VS_TARGET],
    memory_manager=solutions_memory_manager,
    dependencies=["seaborn", "pandas", "matplotlib"],
)

numerical_vs_target_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.NUMERICAL_VS_TARGET],
    memory_manager=solutions_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas", "numpy"],
)

missing_value_imputation_strategy_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[
        EdaSubTask.MISSING_VALUE_IMPUTATION_STRATEGY
    ],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas", "sklearn.impute", "numpy"],
)

class_distribution_check_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.CLASS_DISTRIBUTION_CHECK],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas", "matplotlib", "seaborn", "imbalanced-learn", "imblearn"],
)

heatmaps_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.HEATMAPS],
    memory_manager=solutions_memory_manager,
    dependencies=["seaborn", "matplotlib", "numpy", "pandas"],
)

time_series_analysis_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.TIME_SERIES_ANALYSIS],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas", "numpy", "statsmodels", "matplotlib"],
)

data_provenance_check_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.DATA_PROVENANCE_CHECK],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas"],
)

log_transformation_check_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.LOG_TRANSFORMATION_CHECK],
    memory_manager=solutions_memory_manager,
    dependencies=["numpy", "pandas", "matplotlib"],
)

data_completeness_check_solution_planner = BaseSolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt_template=EDA_REFLECTION_PROMPTS[EdaSubTask.DATA_COMPLETENESS_CHECK],
    memory_manager=solutions_memory_manager,
    dependencies=["pandas", "numpy"],
)
