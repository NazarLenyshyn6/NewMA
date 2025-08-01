"""..."""

CLASSIFICATION_SUBTASK_EXAMPLES = [
    {
        "question": "How can I encode categorical variables like 'Gender' or 'Country'?",
        "subtasks": "CATEGORICAL_ENCODING",
    },
    {
        "question": "Should I normalize or standardize my features before training a model?",
        "subtasks": "FEATURE_SCALING",
    },
    {
        "question": "How do I choose which features to use for my classifier?",
        "subtasks": "FEATURE_SELECTION",
    },
    {
        "question": "How do I split my data into training and testing sets?",
        "subtasks": "DATA_SPLITTING",
    },
    {
        "question": "Which classification algorithm should I use for predicting churn?",
        "subtasks": "MODEL_SELECTION",
    },
    {
        "question": "Train a Random Forest classifier on my dataset.",
        "subtasks": "TRAINING",
    },
    {
        "question": "How can I tune the hyperparameters of my XGBoost model?",
        "subtasks": "HYPERPARAMETER_TUNING",
    },
    {
        "question": "Evaluate the performance of my classifier on the test set.",
        "subtasks": "MODEL_EVALUATION",
    },
    {
        "question": "Apply cross-validation to validate model robustness.",
        "subtasks": "CROSS_VALIDATION",
    },
    {
        "question": "Which performance metrics should I use for classification?",
        "subtasks": "PERFORMANCE_METRICS",
    },
    {
        "question": "Can you compute and plot the confusion matrix?",
        "subtasks": "CONFUSION_MATRIX",
    },
    {
        "question": "Which features are most important for my classifier?",
        "subtasks": "FEATURE_IMPORTANCE",
    },
    {
        "question": "How do I explain the predictions of my model to stakeholders?",
        "subtasks": "MODEL_EXPLANATION",
    },
    {
        "question": "Save the trained model to disk for later use.",
        "subtasks": "MODEL_SERIALIZATION",
    },
    {
        "question": "How can I monitor my model’s performance in production?",
        "subtasks": "MONITORING",
    },
    {"question": "Who won the Champions League in 2023?", "subtasks": "OTHER"},
    {"question": "Build an app to manage my personal finance.", "subtasks": "OTHER"},
]
