"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class SolutionPlanningPromptTemplate:
    """..."""

    @staticmethod
    def build(system_prompt: str) -> ChatPromptTemplate:
        """..."""
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    system_prompt + "\n\n"
                    "You are a highly capable ML engineer assistant helping users solve practical machine learning "
                    "and data analysis problems. Your role is to produce clear, step-by-step plain-text plans "
                    "to approach the user’s problem efficiently and logically. "
                    "Do not include code. Do not mention code. Do not include data ingestion steps. "
                    "Assume the data is already imported and available."
                ),
                HumanMessagePromptTemplate.from_template(
                    "Here is the previous context (if any):\n\n"
                    "{history}\n\n"
                    "Use this context to understand the problem more deeply."
                ),
                HumanMessagePromptTemplate.from_template(
                    "User question:\n{question}\n\n"
                    "Generate a concise and well-structured step-by-step plan to address the question. "
                    "Focus only on high-level, practical steps related to data analysis or modeling. "
                    "Exclude any data ingestion or code-related content. Only provide plain-text guidance."
                ),
            ]
        )


# Example Output (From the Agent):
# Step-by-step plan to address the question:
# Review the structure of the dataset to understand feature types and target variable.
# Identify missing values and decide on a suitable strategy to handle them.
# Perform exploratory data analysis (EDA) to uncover patterns, correlations, and outliers.
# Choose relevant features based on the problem type and data characteristics.
# Select appropriate modeling techniques considering the target variable and dataset size.
# Define an evaluation strategy (e.g., cross-validation, metrics) suitable for the problem.
# Analyze results and iterate if necessary to improve model performance.
# Summarize findings and next steps for the user.
