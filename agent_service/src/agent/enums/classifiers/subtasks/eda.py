"""..."""

from enum import Enum, auto


class EdaSubTasks(Enum):
    """..."""

    # ─────── 1. Data Quality and Consistency ───────
    MISSING_VALUES_DETECTION = auto()
    MISSING_VALUE_IMPUTATION_STRATEGY = auto()
    DUPLICATE_ROWS_DETECTION = auto()
    INCONSISTENT_DATA_TYPES = auto()
    INVALID_CATEGORIES_DETECTION = auto()
    CONSTANT_FEATURES_DETECTION = auto()
    MIXED_TYPE_COLUMN_DETECTION = auto()
    NON_STANDARD_DATE_PARSING = auto()
    COLUMN_NAME_SANITIZATION = auto()
    FEATURE_NAME_DUPLICATION_CHECK = auto()
    INDEX_VALIDITY_CHECK = auto()

    # ─────── 2. Basic Dataset Overview ───────
    DATA_SHAPE_OVERVIEW = auto()
    SAMPLE_INSPECTION = auto()
    UNIQUE_VALUES_ANALYSIS = auto()
    FEATURE_CARDINALITY_SUMMARY = auto()
    STATISTICAL_SUMMARY = auto()
    VALUE_COUNTS_PER_COLUMN = auto()
    CLASS_DISTRIBUTION_CHECK = auto()
    FEATURE_TYPES_SUMMARY = auto()

    # ─────── 3. Statistical Tests ───────
    NORMALITY_TEST = auto()  # Shapiro-Wilk, Anderson-Darling
    EQUAL_VARIANCE_TEST = auto()  # Levene, Bartlett
    CHI_SQUARE_TEST_FOR_CATEGORICALS = auto()
    ANOVA_TEST = auto()
    T_TEST = auto()
    MANN_WHITNEY_TEST = auto()
    KS_TEST = auto()
    FEATURE_INDEPENDENCE_TEST = auto()

    # ─────── 4. Distribution Analysis ───────
    DISTRIBUTION_PLOTS = auto()
    KDE_PLOTS = auto()
    HISTOGRAMS = auto()
    BOXPLOTS = auto()
    VIOLIN_PLOTS = auto()
    SKEWNESS_KURTOSIS_ANALYSIS = auto()
    Q_Q_PLOTS = auto()
    ECDF_PLOTS = auto()
    LOG_TRANSFORM_ANALYSIS = auto()
    SCALING_REQUIREMENT_ANALYSIS = auto()

    # ─────── 5. Outlier & Anomaly Detection ───────
    IQR_OUTLIER_DETECTION = auto()
    Z_SCORE_ANALYSIS = auto()
    DBSCAN_ANOMALY_DETECTION = auto()
    ISOLATION_FOREST_DETECTION = auto()
    LOCAL_OUTLIER_FACTOR = auto()
    OUTLIER_VISUALIZATION = auto()

    # ─────── 6. Correlation & Feature Relationships ───────
    CORRELATION_MATRIX_ANALYSIS = auto()
    PEARSON_CORRELATION = auto()
    SPEARMAN_CORRELATION = auto()
    PHI_COEFFICIENT = auto()
    CRAMERS_V = auto()
    POINT_BISERIAL = auto()
    CORRELATION_HEATMAP = auto()
    MULTICOLLINEARITY_DETECTION = auto()
    VARIANCE_INFLATION_FACTOR = auto()
    REDUNDANT_FEATURE_ANALYSIS = auto()

    # ─────── 7. Bivariate & Multivariate Analysis ───────
    SCATTER_PLOTS = auto()
    PAIR_PLOTS = auto()
    NUMERICAL_VS_TARGET = auto()
    CATEGORICAL_VS_TARGET = auto()
    GROUPED_BOXPLOTS = auto()
    INTERACTION_PLOTS = auto()
    FEATURE_TARGET_RELATIONSHIP = auto()

    # ─────── 8. Categorical Features Deep Dive ───────
    LEVEL_COUNTS = auto()
    DOMINANT_CATEGORY_ANALYSIS = auto()
    RARE_LABEL_DETECTION = auto()
    TARGET_MEAN_ENCODING_INSPECTION = auto()
    CATEGORICAL_ENCODING_STRATEGY_SUGGESTION = auto()

    # ─────── 9. Time Series Exploration ───────
    TIME_INDEX_VALIDATION = auto()
    TIME_GAPS_DETECTION = auto()
    TREND_SEASONALITY_ANALYSIS = auto()
    STATIONARITY_CHECK = auto()
    ACF_PACF_ANALYSIS = auto()
    TIME_BASED_AGGREGATION = auto()
    LAG_FEATURE_SUGGESTION = auto()
    TEMPORAL_HEATMAPS = auto()

    # ─────── 10. Feature Engineering Candidates ───────
    FEATURE_SCALING_ANALYSIS = auto()
    POLYNOMIAL_FEATURE_EXPLORATION = auto()
    BINNING_FEASIBILITY_CHECK = auto()
    TEXT_LENGTH_FEATURE_CANDIDATE = auto()
    DATETIME_FEATURE_EXTRACTION = auto()
    DOMAIN_KNOWLEDGE_FEATURE_SUGGESTION = auto()
    FEATURE_CLUSTERING = auto()
    DIMENSIONALITY_REDUCTION_FEASIBILITY = auto()

    # ─────── 11. Dimensionality Reduction & Latent Structure ───────
    PCA_COMPONENT_ANALYSIS = auto()
    T_SNE_VISUALIZATION = auto()
    UMAP_VISUALIZATION = auto()
    CLUSTER_TENDENCY_EVALUATION = auto()
    HIERARCHICAL_CLUSTER_INSPECTION = auto()

    # ─────── 12. Summary Reports ───────
    HEATMAPS = auto()
    INTERACTIVE_EDA_DASHBOARD = auto()
    FEATURE_SUMMARY_REPORT = auto()
    TARGET_DISTRIBUTION_REPORT = auto()
    AUTO_EDA_PROFILE_REPORT = auto()

    # MISSING_VALUES = auto()
    # DUPLICATE_ROWS_DETECTION = auto()
    # DATA_TYPES_CHECK = auto()
    # UNIQUE_VALUES_ANALYSIS = auto()
    # STATISTICAL_SUMMARY = auto()
    # DISTRIBUTION_ANALYSIS = auto()
    # OUTLIER_DETECTION = auto()
    # CORRELATION_ANALYSIS = auto()
    # PAIR_PLOTS = auto()
    # CATEGORICAL_VS_TARGET = auto()
    # NUMERICAL_VS_TARGET = auto()
    # MISSING_VALUE_IMPUTATION_STRATEGY = auto()
    # CLASS_DISTRIBUTION_CHECK = auto()
    # HEATMAPS = auto()
    # TIME_SERIES_ANALYSIS = auto()
    # DATA_PROVENANCE_CHECK = auto()
    # LOG_TRANSFORMATION_CHECK = auto()
    # DATA_COMPLETENESS_CHECK = auto()
