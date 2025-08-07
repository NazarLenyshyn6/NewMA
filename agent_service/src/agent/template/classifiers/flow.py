"""..."""

from typing import List, Dict

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class FlowClassificationPromptTemplate:
    """..."""

    @staticmethod
    def build() -> ChatPromptTemplate:
        """..."""
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are a classification assistant that determines whether a user’s question requires:\n\n"
                    "**EXECUTE**: Generate code, run analysis, or take direct action on data (e.g., train a model, impute missing values, create a chart)\n"
                    "**EXPLAIN**: Reason about, explain, or summarize previously done work without generating new code or taking action\n\n"
                    "**CLASSIFICATION RULES:**\n"
                    "1. Classify as **EXECUTE** ONLY if the user gives a clear and directed instruction to perform a task (e.g., 'train XGBoost on this data', 'run EDA', 'show histogram').\n"
                    "2. If the user asks a question about previously done work (e.g., 'why was X chosen?', 'is my model stable?'), classify as **EXPLAIN**.\n"
                    "3. If the user asks a vague or general ML-related question (e.g., 'can you do classification?', 'can you analyze this?'), classify as **EXPLAIN**.\n"
                    "4. If the question is ambiguous or unclear, ALWAYS default to **EXPLAIN**.\n"
                    "5. NEVER assume code is needed unless the instruction is specific, actionable, and clearly expressed.\n\n"
                    "**OUTPUT FORMAT:**\n"
                    "- Respond with ONE word only: `EXECUTE` or `EXPLAIN`\n"
                    "- Do NOT include any justification or explanation.\n"
                    "- Do NOT output anything else."
                ),
                HumanMessagePromptTemplate.from_template(
                    "User Question:\n{question}\n\n"
                    "Classify this question conservatively as EXECUTE or EXPLAIN."
                ),
            ]
        )
