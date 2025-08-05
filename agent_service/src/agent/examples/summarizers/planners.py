""""""

solution_plans_summarization_examples = [
    # Example 1: starting from empty summary and adding Steps 1 and 2
    {
        "summary": "",
        "new_solutions": (
            "Step 1: Numeric central tendency and dispersion analysis\n"
            "  Why: Calculate comprehensive descriptive statistics for all numeric variables\n"
            "  Finding: Computed statistics for 5 numeric columns including mean, median, std, variance, range, and IQR\n"
            "  Action: Generated complete descriptive statistics dictionary for numeric variables\n\n"
            "Step 2: Distribution shape analysis\n"
            "  Why: Assess skewness and kurtosis to understand distribution characteristics\n"
            "  Finding: Analyzed shape metrics for 5 numeric variables with interpretations\n"
            "  Action: Computed skewness and kurtosis with categorical interpretations for transformation planning"
        ),
        "updated_summary": (
            "Initial analysis focused on numeric variables, computing comprehensive descriptive statistics such as mean, median, "
            "and dispersion metrics to establish baseline understanding. Distribution shape was further assessed using skewness "
            "and kurtosis, revealing patterns that inform necessary data transformations to improve normality assumptions and modeling."
        ),
    },
    # Example 2: from previous summary, add Steps 3 and 4
    {
        "summary": (
            "Initial analysis focused on numeric variables, computing comprehensive descriptive statistics such as mean, median, "
            "and dispersion metrics to establish baseline understanding. Distribution shape was further assessed using skewness "
            "and kurtosis, revealing patterns that inform necessary data transformations to improve normality assumptions and modeling."
        ),
        "new_solutions": (
            "Step 3: Categorical frequency distribution analysis\n"
            "  Why: Examine frequency patterns and identify dominant/rare categories in categorical variables\n"
            "  Finding: Generated frequency distributions for 6 categorical columns with rare category identification\n"
            "  Action: Computed comprehensive frequency statistics including most/least frequent values and rare category counts\n\n"
            "Step 4: Percentile distribution analysis\n"
            "  Why: Calculate detailed percentile distributions to understand data concentration and spread patterns\n"
            "  Finding: Generated percentile distributions for 5 numeric variables including deciles and extreme percentiles\n"
            "  Action: Computed comprehensive percentile analysis for threshold identification and business rule development"
        ),
        "updated_summary": (
            "Building on numeric analysis, categorical variables were profiled to understand frequency distributions, "
            "highlighting dominant and rare categories critical for encoding strategies. Percentile distributions were also "
            "analyzed in detail, providing granular insight into data spread that supports threshold setting and rule-based feature engineering."
        ),
    },
    # Example 3: from previous summary, add Steps 5 and 6
    {
        "summary": (
            "Building on numeric analysis, categorical variables were profiled to understand frequency distributions, "
            "highlighting dominant and rare categories critical for encoding strategies. Percentile distributions were also "
            "analyzed in detail, providing granular insight into data spread that supports threshold setting and rule-based feature engineering."
        ),
        "new_solutions": (
            "Step 5: Statistical outlier detection analysis\n"
            "  Why: Identify outliers using multiple statistical methods to distinguish extreme values from data errors\n"
            "  Finding: Detected outliers in 5 numeric variables using z-score, modified z-score, and IQR methods\n"
            "  Action: Applied comprehensive outlier detection with multiple statistical approaches and percentage calculations\n\n"
            "Step 6: Distribution normality assessment\n"
            "  Why: Test normality assumptions using statistical tests to guide analytical approach selection\n"
            "  Finding: Performed normality tests on 5 numeric variables using Shapiro-Wilk and Jarque-Bera tests\n"
            "  Action: Conducted comprehensive normality testing with consensus determination for transformation recommendations"
        ),
        "updated_summary": (
            "Outlier detection was robustly applied using multiple statistical techniques to differentiate true anomalies from errors, "
            "ensuring data integrity. Concurrently, normality tests confirmed distribution characteristics, informing the necessity "
            "of targeted transformations to satisfy model assumptions and optimize predictive performance."
        ),
    },
    # Example 4: from previous summary, add Step 7
    {
        "summary": (
            "Outlier detection was robustly applied using multiple statistical techniques to differentiate true anomalies from errors, "
            "ensuring data integrity. Concurrently, normality tests confirmed distribution characteristics, informing the necessity "
            "of targeted transformations to satisfy model assumptions and optimize predictive performance."
        ),
        "new_solutions": (
            "Step 7: Bivariate correlation analysis\n"
            "  Why: Examine relationships between numeric variables to identify multicollinearity and dependency patterns\n"
            "  Finding: Computed correlation matrix for 5 variables with 0 high correlations detected\n"
            "  Action: Generated comprehensive correlation analysis with high correlation identification for multicollinearity assessment"
        ),
        "updated_summary": (
            "The analysis culminates with bivariate correlation assessment, which found no significant multicollinearity among numeric features. "
            "This ensures model stability and simplifies feature selection, confirming readiness for subsequent modeling and validation steps."
        ),
    },
]
