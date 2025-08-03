"""..."""

from agent.runners.planners import SolutionPlanningRunner
from agent.enums.classifiers.subtasks.eda import EdaSubTasks
from agent.enums.classifiers.subtasks.classification import ClassificationSubTasks
from agent.registry.planners import eda as eda_planners
from agent.registry.planners import classification as classification_subtasks
from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model


planners = {
    EdaSubTasks.MISSING_VALUES.name: eda_planners.missing_values_solution_planner,
    EdaSubTasks.DUPLICATE_ROWS_DETECTION.name: eda_planners.duplicate_rows_detection_solution_planner,
    EdaSubTasks.DATA_TYPES_CHECK.name: eda_planners.data_types_check_solution_planner,
    EdaSubTasks.UNIQUE_VALUES_ANALYSIS.name: eda_planners.unique_values_analysis_solution_planner,
    EdaSubTasks.STATISTICAL_SUMMARY.name: eda_planners.statistical_summary_solution_planner,
    EdaSubTasks.DISTRIBUTION_ANALYSIS.name: eda_planners.distribution_analysis_solution_planner,
    EdaSubTasks.OUTLIER_DETECTION.name: eda_planners.outlier_detection_solution_planner,
    EdaSubTasks.CORRELATION_ANALYSIS.name: eda_planners.correlation_analysis_solution_planner,
    EdaSubTasks.PAIR_PLOTS.name: eda_planners.pair_plots_solution_planner,
    EdaSubTasks.CATEGORICAL_VS_TARGET.name: eda_planners.categorical_vs_target_solution_planner,
    EdaSubTasks.NUMERICAL_VS_TARGET.name: eda_planners.numerical_vs_target_solution_planner,
    EdaSubTasks.MISSING_VALUE_IMPUTATION_STRATEGY.name: eda_planners.missing_value_imputation_strategy_solution_planner,
    EdaSubTasks.CLASS_DISTRIBUTION_CHECK.name: eda_planners.class_distribution_check_solution_planner,
    EdaSubTasks.HEATMAPS.name: eda_planners.heatmaps_solution_planner,
    EdaSubTasks.TIME_SERIES_ANALYSIS.name: eda_planners.time_series_analysis_solution_planner,
    EdaSubTasks.DATA_PROVENANCE_CHECK.name: eda_planners.data_provenance_check_solution_planner,
    EdaSubTasks.LOG_TRANSFORMATION_CHECK.name: eda_planners.log_transformation_check_solution_planner,
    EdaSubTasks.DATA_COMPLETENESS_CHECK.name: eda_planners.data_completeness_check_solution_planner,
}

solution_planning_runner = SolutionPlanningRunner(
    model=anthropic_claude_sonnet_4_20250514_model, planners=planners
)
