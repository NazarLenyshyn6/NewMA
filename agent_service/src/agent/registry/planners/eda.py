"""..."""

from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.registry.memory.planners import solution_planner_memory_manager
from agent.planners import SolutionPlanner
from agent.prompts.planners import eda


missing_values_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.missing_values_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

missing_value_imputation_strategy_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.missing_value_imputation_strategy_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "sklearn"],
)

duplicate_rows_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.duplicate_rows_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

inconsistent_data_types_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.inconsistent_data_types_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

invalid_categories_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.invalid_categories_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

constant_features_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.constant_features_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

mixed_type_column_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.mixed_type_column_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

non_standard_date_parsing_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.non_standard_date_parsing_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "dateutil"],
)

column_name_sanitization_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.column_name_sanitization_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "re"],
)

feature_name_duplication_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.feature_name_duplication_check_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

index_validity_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.index_validity_check_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

data_shape_overview_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.data_shape_overview_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

sample_inspection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.sample_inspection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

unique_values_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.unique_values_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

feature_cardinality_summary_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.feature_cardinality_summary_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

pca_component_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.pca_component_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "numpy", "pandas"],
)

statistical_summary_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.statistical_summary_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "scipy"],
)

value_counts_per_column_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.value_counts_per_column_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

class_distribution_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.class_distribution_check_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "matplotlib", "seaborn", "imblearn"],
)

feature_types_summary_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.feature_types_summary_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

normality_test_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.normality_test_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "numpy", "pandas"],
)

equal_variance_test_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.equal_variance_test_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "numpy", "pandas"],
)

chi_square_test_for_categoricals_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.chi_square_test_for_categoricals_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "pandas", "numpy"],
)


anova_test_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.anova_test_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "statsmodels", "numpy", "pandas"],
)

t_test_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.t_test_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "numpy", "pandas"],
)

mann_whitney_test_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.mann_whitney_test_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "numpy", "pandas"],
)

ks_test_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.ks_test_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "numpy", "pandas"],
)

feature_independence_test_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.feature_independence_test_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "pandas", "numpy"],
)

distribution_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.distribution_plots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas", "numpy"],
)

kde_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.kde_plots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "matplotlib", "pandas"],
)

histograms_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.histograms_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas"],
)

boxplots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.boxplots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas"],
)

violin_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.violin_plots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas"],
)

skewness_kurtosis_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.skewness_kurtosis_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "pandas", "numpy"],
)

q_q_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.q_q_plots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["statsmodels", "matplotlib", "scipy", "pandas"],
)

ecdf_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.ecdf_plots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "numpy", "pandas"],
)

log_transform_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.log_transform_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["numpy", "pandas", "matplotlib"],
)

scaling_requirement_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.scaling_requirement_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "sklearn"],
)

iqr_outlier_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.iqr_outlier_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["numpy", "pandas"],
)

z_score_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.z_score_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["numpy", "pandas"],
)

dbscan_anomaly_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.dbscan_anomaly_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "numpy", "pandas"],
)

isolation_forest_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.isolation_forest_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "numpy", "pandas"],
)

local_outlier_factor_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.local_outlier_factor_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "numpy", "pandas"],
)

outlier_visualization_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.outlier_visualization_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas"],
)

correlation_matrix_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.correlation_matrix_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "scipy"],
)

pearson_correlation_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.pearson_correlation_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "numpy", "pandas"],
)

spearman_correlation_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.spearman_correlation_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "numpy", "pandas"],
)

phi_coefficient_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.phi_coefficient_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "scipy"],
)

cramers_v_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.cramers_v_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "scipy"],
)

point_biserial_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.point_biserial_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "numpy", "pandas"],
)

correlation_heatmap_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.correlation_heatmap_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "matplotlib", "pandas", "numpy"],
)

multicollinearity_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.multicollinearity_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "statsmodels"],
)

variance_inflation_factor_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.variance_inflation_factor_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["statsmodels", "pandas", "numpy"],
)

redundant_feature_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.redundant_feature_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "sklearn"],
)

scatter_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.scatter_plots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas"],
)

pair_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.pair_plots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "matplotlib", "pandas"],
)

numerical_vs_target_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.numerical_vs_target_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas", "numpy"],
)

categorical_vs_target_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.categorical_vs_target_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "pandas", "matplotlib"],
)

grouped_boxplots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.grouped_boxplots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "matplotlib", "pandas"],
)

interaction_plots_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.interaction_plots_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas", "statsmodels"],
)

feature_target_relationship_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.feature_target_relationship_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "matplotlib", "seaborn"],
)
level_counts_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.level_counts_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas"],
)

dominant_category_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.dominant_category_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

rare_label_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.rare_label_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

target_mean_encoding_inspection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.target_mean_encoding_inspection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "sklearn"],
)

categorical_encoding_strategy_suggestion_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.categorical_encoding_strategy_suggestion_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "category_encoders", "sklearn"],
)

time_index_validation_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.time_index_validation_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

time_gaps_detection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.time_gaps_detection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

trend_seasonality_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.trend_seasonality_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy", "statsmodels", "matplotlib"],
)

stationarity_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.stationarity_check_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["statsmodels", "pandas", "numpy"],
)

acf_pacf_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.acf_pacf_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["statsmodels", "matplotlib", "pandas", "numpy"],
)

time_based_aggregation_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.time_based_aggregation_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

lag_feature_suggestion_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.lag_feature_suggestion_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

temporal_heatmaps_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.temporal_heatmaps_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "matplotlib", "pandas", "numpy"],
)

feature_scaling_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.feature_scaling_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "pandas", "numpy"],
)

polynomial_feature_exploration_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.polynomial_feature_exploration_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "pandas", "numpy"],
)

binning_feasibility_check_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.binning_feasibility_check_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

text_length_feature_candidate_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.text_length_feature_candidate_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

datetime_feature_extraction_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.datetime_feature_extraction_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

domain_knowledge_feature_suggestion_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.domain_knowledge_feature_suggestion_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

feature_clustering_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.feature_clustering_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "pandas", "numpy", "scipy"],
)

dimensionality_reduction_feasibility_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.dimensionality_reduction_feasibility_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "pandas", "numpy"],
)

ca_component_analysis_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.pca_component_analysis_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "numpy", "pandas"],
)

t_sne_visualization_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.t_sne_visualization_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "matplotlib", "pandas", "numpy"],
)

umap_visualization_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.umap_visualization_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["umap-learn", "matplotlib", "pandas", "numpy"],
)

cluster_tendency_evaluation_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.cluster_tendency_evaluation_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["sklearn", "pandas", "numpy", "scipy"],
)

hierarchical_cluster_inspection_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.hierarchical_cluster_inspection_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["scipy", "matplotlib", "pandas", "numpy"],
)

heatmaps_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.heatmaps_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["seaborn", "matplotlib", "numpy", "pandas"],
)

interactive_eda_dashboard_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.interactive_eda_dashboard_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["plotly", "dash", "pandas", "numpy"],
)

feature_summary_report_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.feature_summary_report_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas", "numpy"],
)

target_distribution_report_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.target_distribution_report_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["matplotlib", "seaborn", "pandas", "numpy"],
)

auto_eda_profile_report_solution_planner = SolutionPlanner(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=eda.auto_eda_profile_report_prompt,
    memory_manager=solution_planner_memory_manager,
    dependencies=["pandas_profiling", "pandas", "numpy"],
)


# missing_values_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.missing_values_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["numpy", "pandas"],
# )

# duplicate_rows_detection_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.duplicate_rows_detection_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas"],
# )

# data_types_check_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.data_types_check_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas", "numpy"],
# )

# unique_values_analysis_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.unique_values_analysis_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas"],
# )

# statistical_summary_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.statistical_summary_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas", "numpy", "scipy"],
# )

# distribution_analysis_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.distribution_analysis_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["matplotlib", "seaborn", "scipy", "numpy"],
# )

# outlier_detection_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.outliers_detection_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["numpy", "scipy", "pandas"],
# )

# correlation_analysis_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.correlation_analysis_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas", "numpy", "seaborn", "matplotlib"],
# )

# pair_plots_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.pair_plots_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["seaborn", "matplotlib", "pandas"],
# )

# categorical_vs_target_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.categorical_vs_target_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["seaborn", "pandas", "matplotlib"],
# )

# numerical_vs_target_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.numerical_vs_target_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["matplotlib", "seaborn", "pandas", "numpy"],
# )

# missing_value_imputation_strategy_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.missing_value_imputation_stragety_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas", "sklearn", "numpy"],
# )

# class_distribution_check_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.class_distribution_check_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas", "matplotlib", "seaborn", "imblearn"],
# )

# heatmaps_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.heatmaps_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["seaborn", "matplotlib", "numpy", "pandas"],
# )

# time_series_analysis_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.time_series_analysis_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas", "numpy", "statsmodels", "matplotlib"],
# )

# data_provenance_check_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.data_provenance_check_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas"],
# )

# log_transformation_check_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.log_transformation_check_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["numpy", "pandas", "matplotlib"],
# )

# data_completeness_check_solution_planner = SolutionPlanner(
#     model=anthropic_claude_sonnet_4_20250514_model,
#     prompt=eda.data_completeness_check_solution_planning_prompt,
#     memory_manager=solution_planner_memory_manager,
#     dependencies=["pandas", "numpy"],
# )
