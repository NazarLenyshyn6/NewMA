"""..."""

EDA_SUBTASK_SELECTION_EXAMPLES = [
    {
        "question": "How many missing values are in my dataset?",
        "subtask": "MISSING_VALUES",
    },
    {
        "question": "Are there any outliers in this data?",
        "subtask": "OUTLIER_DETECTION",
    },
    {
        "question": "What is the distribution of my target variable?",
        "subtask": "DISTRIBUTION_ANALYSIS",
    },
    {
        "question": "Which features are most correlated with the outcome?",
        "subtask": "CORRELATION_ANALYSIS",
    },
    {
        "question": "Please summarize the dataset before modeling.",
        "subtask": "DATA_OVERVIEW",
    },
    {
        "question": "Can you show the relationships between variables?",
        "subtask": "RELATIONSHIP_ANALYSIS",
    },
    {
        "question": "Explore the range and distribution of features.",
        "subtask": "DISTRIBUTION_ANALYSIS",
    },
    {
        "question": "Detect and handle missing or anomalous data.",
        "subtask": "MISSING_VALUES, OUTLIER_DETECTION",
    },
    {
        "question": "How can I check for multicollinearity?",
        "subtask": "CORRELATION_ANALYSIS",
    },
    {
        "question": "Give me insights before any modeling.",
        "subtask": "DATA_OVERVIEW, DISTRIBUTION_ANALYSIS, CORRELATION_ANALYSIS",
    },
    {"question": "How can I know if I’m getting fat?", "subtasks": "OTHER"},
    {
        "question": "Build a dashboard for marketing team to explore website traffic",
        "subtasks": "OTHER",
    },
]
