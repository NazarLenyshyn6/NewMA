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
                    "- Use ONLY the following libraries: {dependencies}"
                    "- DO NOT use any library that is not explicitly allowed or already imported\n"
                    "- DO NOT repeat or redefine any transformations summarized below\n"
                    "- DO NOT write modularized, abstracted, or commented code — output only raw Python code that is direct and efficient\n"
                    "- DO NOT include any text, markdown, or explanations — only executable Python code\n"
                    "- All logic MUST be based on the current dataset structure and existing variables\n\n"
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
                    "- As short and efficient as possible\n"
                    "- Continues seamlessly from the prior code state"
                ),
            ]
        )
