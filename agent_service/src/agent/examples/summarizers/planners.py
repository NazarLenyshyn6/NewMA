"""..."""

solution_plans_summarization_examples = [
    # Example 1: starting from empty summary and first chunk (Step 1 and Step 2)
    {
        "summary": "",
        "new_solutions": (
            "# Data Type Validation and Outlier Removal Plan\n\n"
            "**Step 1: Data Inspection and Type Assessment**\n"
            "- Load dataset, profile data, generate schema report, identify incorrect data types, "
            "document baseline quality\n\n"
            "**Step 2: Data Type Validation and Correction**\n"
            "- Validate and convert types systematically including numeric, datetime, categorical, boolean, "
            "document all changes"
        ),
        "updated_summary": (
            "The plan begins with thorough data inspection and profiling to identify type issues and establish a baseline. "
            "It then implements systematic validation and correction of data types including numerics, dates, categoricals, "
            "and booleans with detailed documentation."
        ),
    },
    # Example 2: from previous summary, add Steps 3 and 4
    {
        "summary": (
            "The plan begins with thorough data inspection and profiling to identify type issues and establish a baseline. "
            "It then implements systematic validation and correction of data types including numerics, dates, categoricals, "
            "and booleans with detailed documentation."
        ),
        "new_solutions": (
            "**Step 3: Missing Value Analysis and Strategy**\n"
            "- Analyze missingness patterns and causes, distinguish structural vs quality issues, "
            "apply imputation by data type, document decisions\n\n"
            "**Step 4: Outlier Detection Framework Implementation**\n"
            "- Use multi-method outlier detection including IQR, Z-score, Modified Z-score, Isolation Forest, "
            "and domain-specific business rules"
        ),
        "updated_summary": (
            "Following type corrections, the plan analyzes missing data thoroughly and applies tailored imputation strategies "
            "while documenting all choices. It then establishes a robust multi-method outlier detection framework combining "
            "statistical methods and machine learning models with domain-specific validations."
        ),
    },
    # You can add more examples progressively including Steps 5-9 similarly.
]
