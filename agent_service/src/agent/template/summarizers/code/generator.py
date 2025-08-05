"""..."""

from typing import List, Dict

from langchain.prompts import PromptTemplate, FewShotPromptTemplate


class GeneratedCodeSummarizationPromptTemplate:
    """..."""

    @staticmethod
    def build(examples: List[Dict[str, str]]) -> FewShotPromptTemplate:
        """..."""
        example_prompt = PromptTemplate(
            input_variables=["summary", "generated_code", "updated_summary"],
            template=(
                "### EXAMPLE\n"
                "Current summary:\n"
                "{summary}\n\n"
                "New lines:\n"
                "{generated_code}\n\n"
                "New summary:\n"
                "{updated_summary}\n"
            ),
        )

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=(
                "You are an expert ML coding assistant. Your task is to progressively summarize a Python ML codebase.\n\n"
                "Each time new code is added, your summary must contain:\n"
                "returning a concise and updated summary."
                "2. A **flat list of all variables that are initialized and will remain after executing the code via `exec()`**.\n\n"
                "❌ Strictly do NOT include:\n"
                "- Imported modules or classes (e.g., `pd`, `np`, `SimpleImputer`)\n"
                "- Loop variables (e.g., `i`, `col`, etc.)\n"
                "- Function parameters\n"
                "- In-line or temporary variables used within comprehensions or conditions\n"
                "- Any code or syntax — summary only\n\n"
                "✅ Do include:\n"
                "- Only actual variables stored in memory that can be accessed after running the code\n"
                "- Variables created conditionally, if they are assigned and retained\n"
            ),
            suffix=(
                "### YOUR TURN\n"
                "Current summary:\n"
                "{summary}\n\n"
                "New lines:\n"
                "{generated_code}\n\n"
                "New summary:"
            ),
            input_variables=["summary", "generated_code"],
        )
