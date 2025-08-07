"""..."""

from agent.runners.planners import SolutionPlanningRunner
from agent.enums.classifiers.subtasks.eda import EdaSubTasks
from agent.enums.classifiers.subtasks.classification import ClassificationSubTasks
from agent.registry.planners import eda as eda_planners
from agent.registry.planners import classification as classification_subtasks
from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model


planners = {
    # Example: mapping enum names to solution planners
    # ─────── 1. Data Quality and Consistency ───────
    "MISSING_VALUES_DETECTION": eda_planners.missing_values_detection_solution_planner,
    "MISSING_VALUE_IMPUTATION_STRATEGY": eda_planners.missing_value_imputation_strategy_solution_planner,
    "DUPLICATE_ROWS_DETECTION": eda_planners.duplicate_rows_detection_solution_planner,
    "INCONSISTENT_DATA_TYPES": eda_planners.inconsistent_data_types_solution_planner,
    "INVALID_CATEGORIES_DETECTION": eda_planners.invalid_categories_detection_solution_planner,
    "CONSTANT_FEATURES_DETECTION": eda_planners.constant_features_detection_solution_planner,
    "MIXED_TYPE_COLUMN_DETECTION": eda_planners.mixed_type_column_detection_solution_planner,
    "NON_STANDARD_DATE_PARSING": eda_planners.non_standard_date_parsing_solution_planner,
    "COLUMN_NAME_SANITIZATION": eda_planners.column_name_sanitization_solution_planner,
    "FEATURE_NAME_DUPLICATION_CHECK": eda_planners.feature_name_duplication_check_solution_planner,
    "INDEX_VALIDITY_CHECK": eda_planners.index_validity_check_solution_planner,
    # ─────── 2. Basic Dataset Overview ───────
    "DATA_SHAPE_OVERVIEW": eda_planners.data_shape_overview_solution_planner,
    "SAMPLE_INSPECTION": eda_planners.sample_inspection_solution_planner,
    "UNIQUE_VALUES_ANALYSIS": eda_planners.unique_values_analysis_solution_planner,
    "FEATURE_CARDINALITY_SUMMARY": eda_planners.feature_cardinality_summary_solution_planner,
    "STATISTICAL_SUMMARY": eda_planners.statistical_summary_solution_planner,
    "VALUE_COUNTS_PER_COLUMN": eda_planners.value_counts_per_column_solution_planner,
    "CLASS_DISTRIBUTION_CHECK": eda_planners.class_distribution_check_solution_planner,
    "FEATURE_TYPES_SUMMARY": eda_planners.feature_types_summary_solution_planner,
    # ─────── 3. Statistical Tests ───────
    "NORMALITY_TEST": eda_planners.normality_test_solution_planner,
    "EQUAL_VARIANCE_TEST": eda_planners.equal_variance_test_solution_planner,
    "CHI_SQUARE_TEST_FOR_CATEGORICALS": eda_planners.chi_square_test_for_categoricals_solution_planner,
    "ANOVA_TEST": eda_planners.anova_test_solution_planner,
    "T_TEST": eda_planners.t_test_solution_planner,
    "MANN_WHITNEY_TEST": eda_planners.mann_whitney_test_solution_planner,
    "KS_TEST": eda_planners.ks_test_solution_planner,
    "FEATURE_INDEPENDENCE_TEST": eda_planners.feature_independence_test_solution_planner,
    # ─────── 4. Distribution Analysis ───────
    "DISTRIBUTION_PLOTS": eda_planners.distribution_plots_solution_planner,
    "KDE_PLOTS": eda_planners.kde_plots_solution_planner,
    "HISTOGRAMS": eda_planners.histograms_solution_planner,
    "BOXPLOTS": eda_planners.boxplots_solution_planner,
    "VIOLIN_PLOTS": eda_planners.violin_plots_solution_planner,
    "SKEWNESS_KURTOSIS_ANALYSIS": eda_planners.skewness_kurtosis_analysis_solution_planner,
    "Q_Q_PLOTS": eda_planners.q_q_plots_solution_planner,
    "ECDF_PLOTS": eda_planners.ecdf_plots_solution_planner,
    "LOG_TRANSFORM_ANALYSIS": eda_planners.log_transform_analysis_solution_planner,
    "SCALING_REQUIREMENT_ANALYSIS": eda_planners.scaling_requirement_analysis_solution_planner,
    # ─────── 5. Outlier & Anomaly Detection ───────
    "IQR_OUTLIER_DETECTION": eda_planners.iqr_outlier_detection_solution_planner,
    "Z_SCORE_ANALYSIS": eda_planners.z_score_analysis_solution_planner,
    "DBSCAN_ANOMALY_DETECTION": eda_planners.dbscan_anomaly_detection_solution_planner,
    "ISOLATION_FOREST_DETECTION": eda_planners.isolation_forest_detection_solution_planner,
    "LOCAL_OUTLIER_FACTOR": eda_planners.local_outlier_factor_solution_planner,
    "OUTLIER_VISUALIZATION": eda_planners.outlier_visualization_solution_planner,
    # ─────── 6. Correlation & Feature Relationships ───────
    "CORRELATION_MATRIX_ANALYSIS": eda_planners.correlation_matrix_analysis_solution_planner,
    "PEARSON_CORRELATION": eda_planners.pearson_correlation_solution_planner,
    "SPEARMAN_CORRELATION": eda_planners.spearman_correlation_solution_planner,
    "PHI_COEFFICIENT": eda_planners.phi_coefficient_solution_planner,
    "CRAMERS_V": eda_planners.cramers_v_solution_planner,
    "POINT_BISERIAL": eda_planners.point_biserial_solution_planner,
    "CORRELATION_HEATMAP": eda_planners.correlation_heatmap_solution_planner,
    "MULTICOLLINEARITY_DETECTION": eda_planners.multicollinearity_detection_solution_planner,
    "VARIANCE_INFLATION_FACTOR": eda_planners.variance_inflation_factor_solution_planner,
    "REDUNDANT_FEATURE_ANALYSIS": eda_planners.redundant_feature_analysis_solution_planner,
    # ─────── 7. Bivariate & Multivariate Analysis ───────
    "SCATTER_PLOTS": eda_planners.scatter_plots_solution_planner,
    "PAIR_PLOTS": eda_planners.pair_plots_solution_planner,
    "NUMERICAL_VS_TARGET": eda_planners.numerical_vs_target_solution_planner,
    "CATEGORICAL_VS_TARGET": eda_planners.categorical_vs_target_solution_planner,
    "GROUPED_BOXPLOTS": eda_planners.grouped_boxplots_solution_planner,
    "INTERACTION_PLOTS": eda_planners.interaction_plots_solution_planner,
    "FEATURE_TARGET_RELATIONSHIP": eda_planners.feature_target_relationship_solution_planner,
    # ─────── 8. Categorical Features Deep Dive ───────
    "LEVEL_COUNTS": eda_planners.level_counts_solution_planner,
    "DOMINANT_CATEGORY_ANALYSIS": eda_planners.dominant_category_analysis_solution_planner,
    "RARE_LABEL_DETECTION": eda_planners.rare_label_detection_solution_planner,
    "TARGET_MEAN_ENCODING_INSPECTION": eda_planners.target_mean_encoding_inspection_solution_planner,
    "CATEGORICAL_ENCODING_STRATEGY_SUGGESTION": eda_planners.categorical_encoding_strategy_suggestion_solution_planner,
    # ─────── 9. Time Series Exploration ───────
    "TIME_INDEX_VALIDATION": eda_planners.time_index_validation_solution_planner,
    "TIME_GAPS_DETECTION": eda_planners.time_gaps_detection_solution_planner,
    "TREND_SEASONALITY_ANALYSIS": eda_planners.trend_seasonality_analysis_solution_planner,
    "STATIONARITY_CHECK": eda_planners.stationarity_check_solution_planner,
    "ACF_PACF_ANALYSIS": eda_planners.acf_pacf_analysis_solution_planner,
    "TIME_BASED_AGGREGATION": eda_planners.time_based_aggregation_solution_planner,
    "LAG_FEATURE_SUGGESTION": eda_planners.lag_feature_suggestion_solution_planner,
    "TEMPORAL_HEATMAPS": eda_planners.temporal_heatmaps_solution_planner,
    # ─────── 10. Feature Engineering Candidates ───────
    "FEATURE_SCALING_ANALYSIS": eda_planners.feature_scaling_analysis_solution_planner,
    "POLYNOMIAL_FEATURE_EXPLORATION": eda_planners.polynomial_feature_exploration_solution_planner,
    "BINNING_FEASIBILITY_CHECK": eda_planners.binning_feasibility_check_solution_planner,
    "TEXT_LENGTH_FEATURE_CANDIDATE": eda_planners.text_length_feature_candidate_solution_planner,
    "DATETIME_FEATURE_EXTRACTION": eda_planners.datetime_feature_extraction_solution_planner,
    "DOMAIN_KNOWLEDGE_FEATURE_SUGGESTION": eda_planners.domain_knowledge_feature_suggestion_solution_planner,
    "FEATURE_CLUSTERING": eda_planners.feature_clustering_solution_planner,
    "DIMENSIONALITY_REDUCTION_FEASIBILITY": eda_planners.dimensionality_reduction_feasibility_solution_planner,
    # ─────── 11. Dimensionality Reduction & Latent Structure ───────
    "PCA_COMPONENT_ANALYSIS": eda_planners.pca_component_analysis_solution_planner,
    "T_SNE_VISUALIZATION": eda_planners.t_sne_visualization_solution_planner,
    "UMAP_VISUALIZATION": eda_planners.umap_visualization_solution_planner,
    "CLUSTER_TENDENCY_EVALUATION": eda_planners.cluster_tendency_evaluation_solution_planner,
    "HIERARCHICAL_CLUSTER_INSPECTION": eda_planners.hierarchical_cluster_inspection_solution_planner,
    # ─────── 12. Summary Reports ───────
    "HEATMAPS": eda_planners.heatmaps_solution_planner,
    "INTERACTIVE_EDA_DASHBOARD": eda_planners.interactive_eda_dashboard_solution_planner,
    "FEATURE_SUMMARY_REPORT": eda_planners.feature_summary_report_solution_planner,
    "TARGET_DISTRIBUTION_REPORT": eda_planners.target_distribution_report_solution_planner,
    "AUTO_EDA_PROFILE_REPORT": eda_planners.auto_eda_profile_report_solution_planner,
    ClassificationSubTasks.CATEGORICAL_ENCODING.name: classification_subtasks.categorical_encoding_solution_planner,
    ClassificationSubTasks.FEATURE_SCALING.name: classification_subtasks.feature_scaling_solution_planner,
    ClassificationSubTasks.FEATURE_SELECTION.name: classification_subtasks.feature_selection_solution_planner,
    ClassificationSubTasks.DATA_SPLITTING.name: classification_subtasks.data_splitting_solution_planner,
    ClassificationSubTasks.MODEL_SELECTION.name: classification_subtasks.model_selection_solution_planner,
    ClassificationSubTasks.TRAINING.name: classification_subtasks.training_solution_planner,
    ClassificationSubTasks.HYPERPARAMETER_TUNING.name: classification_subtasks.hyperparameter_tuning_solution_planner,
    ClassificationSubTasks.MODEL_EVALUATION.name: classification_subtasks.model_evaluation_solution_planner,
    ClassificationSubTasks.CROSS_VALIDATION.name: classification_subtasks.cross_validation_solution_planner,
    ClassificationSubTasks.CONFUSION_MATRIX.name: classification_subtasks.confusion_matrix_solution_planner,
    ClassificationSubTasks.FEATURE_IMPORTANCE.name: classification_subtasks.feature_importance_solution_planner,
    ClassificationSubTasks.MODEL_EXPLANATION.name: classification_subtasks.model_explanation_solution_planner,
    ClassificationSubTasks.MODEL_SERIALIZATION.name: classification_subtasks.model_serialization_solution_planner,
}

solution_planning_runner = SolutionPlanningRunner(
    model=anthropic_claude_sonnet_4_20250514_model, planners=planners
)
