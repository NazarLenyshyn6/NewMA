"""..."""

from enum import Enum
from agent_core.subtask_selectors.enums.base import BaseSubTask


class EdaSubTask(BaseSubTask, Enum):
    """..."""

    # Data quality checks
    MISSING_VALUES = "missing_values"  # Identify and analyze missing data
    DUPLICATE_ROWS_DETECTION = (
        "duplicate_rows_detection"  # Find duplicate rows in dataset
    )
    DATA_TYPES_CHECK = "data_types_check"  # Verify and correct data types
    UNIQUE_VALUES_ANALYSIS = "unique_values_analysis"  # Check unique values per column

    # Statistical summaries
    STATISTICAL_SUMMARY = "statistical_summary"  # Mean, median, std, quantiles, etc.
    DISTRIBUTION_ANALYSIS = (
        "distribution_analysis"  # Histograms, KDE plots for feature distribution
    )

    # Outlier and anomaly detection
    OUTLIER_DETECTION = "outlier_detection"  # Detect outliers using statistical methods

    # Relationships and correlations
    CORRELATION_ANALYSIS = "correlation_analysis"  # Correlation matrix, heatmaps
    PAIR_PLOTS = "pair_plots"  # Scatterplots for feature pairs

    # Feature-specific analysis
    CATEGORICAL_VS_TARGET = (
        "categorical_vs_target_analysis"  # Boxplots, countplots vs target
    )
    NUMERICAL_VS_TARGET = "numerical_vs_target_analysis"  # Scatterplots, trend analysis

    # Missing value treatment analysis (optional step in EDA)
    MISSING_VALUE_IMPUTATION_STRATEGY = (
        "missing_value_imputation_strategy"  # Decide imputation methods
    )

    # Data distribution and imbalance
    CLASS_DISTRIBUTION_CHECK = (
        "class_distribution_check"  # For classification targets, check imbalance
    )

    # Visualization aids
    HEATMAPS = "heatmaps"  # Visualize correlations, missingness, etc.
    TIME_SERIES_ANALYSIS = "time_series_analysis"  # If dataset has time component

    # Miscellaneous
    DATA_PROVENANCE_CHECK = (
        "data_provenance_check"  # Validate data source and integrity
    )

    # Data transformations exploratory (optional)
    LOG_TRANSFORMATION_CHECK = (
        "log_transformation_check"  # Check skewness, need for log transform
    )

    # Data completeness and coverage
    DATA_COMPLETENESS_CHECK = (
        "data_completeness_check"  # Coverage over key groups or time
    )
