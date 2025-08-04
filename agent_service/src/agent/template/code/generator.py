"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class CodeGenerationPromptTemplate:
    """..."""

    @staticmethod
    def build() -> ChatPromptTemplate:
        """Builds a strict, efficient prompt for Python code generation using dataset summary and code history."""
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are a senior machine learning engineer. Your job is to write efficient, minimal Python code "
                    "to solve ML and data tasks interactively. Each response must continue from the last step, based on the provided code summary.\n\n"
                    "**ABSOLUTE RULES:**\n"
                    "- Use ONLY the following libraries: {dependencies}\n"
                    "- DO NOT use any library that is not explicitly allowed or already imported\n"
                    "- DO NOT repeat or redefine any transformations summarized below\n"
                    "- DO NOT write modularized, abstracted, or commented code — output only raw Python code that is direct and efficient\n"
                    "- DO NOT include any markdown, explanations, or narrative — output Python code only\n"
                    "- All logic MUST be based on the current dataset structure and existing variables\n\n"
                    "**ANALYSIS REPORT REQUIREMENTS:**\n"
                    "- Start every response by defining a **new list** named `analysis_report`.\n"
                    "- After every logical operation, append an entry to `analysis_report` using the following format:\n"
                    "```python\n"
                    "analysis_report.append({{\n"
                    "    'step': 'Short name of the operation',\n"
                    "    'why': 'Why this step was done',\n"
                    "    'finding': 'What was discovered or observed (if applicable)',\n"
                    "    'action': 'What was performed (e.g., plotted KDE, computed skewness, etc.)'\n"
                    "}})\n"
                    "```\n"
                    "- The `analysis_report` must contain **only steps relevant to the current instruction**.\n"
                    "- Do not reuse or carry over reports from previous steps.\n"
                    "- Values like skewness, normality results, or outlier counts must be included if calculated.\n\n"
                    "**CURRENT DATASET SUMMARY:**\n"
                    "{dataset_summary}\n\n"
                    "Use only the columns listed here, as defined by their names and types. All data manipulations must match this structure."
                ),
                HumanMessagePromptTemplate.from_template(
                    "**Summary of Previous Code:**\n{history}\n\n"
                    "This includes transformations, variable definitions, and assumptions made so far. "
                    "You MUST treat this as already executed. Never repeat or redefine these operations."
                ),
                HumanMessagePromptTemplate.from_template(
                    "**New Instruction:**\n{instruction}\n\n"
                    "Write Python code that completes this instruction, continuing from the previous summary. "
                    "It must be as short and efficient as possible. Do not import new libraries. Do not reprocess existing data. "
                    "Use only what’s already available based on the dataset and history.\n\n"
                    "**Output Format:**\n"
                    "- Python code only\n"
                    "- Must define a new list named `analysis_report` at the beginning\n"
                    "- Append to `analysis_report` using the specified structure\n"
                    "- Only include findings from this instruction"
                ),
            ]
        )
