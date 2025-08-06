"""..."""

from typing import List, Dict

from langchain.prompts import PromptTemplate, FewShotPromptTemplate


class GeneratedCodeSummarizationPromptTemplate:
    """..."""

    @staticmethod
    def build(examples: List[Dict[str, str]]) -> FewShotPromptTemplate:
        """Constructs a few-shot prompt for code summarization and state tracking."""
        example_prompt = PromptTemplate(
            input_variables=[
                "task_type",
                "summary",
                "generated_code",
                "updated_summary",
            ],
            template=(
                "### EXAMPLE\n"
                "Previous Summary:\n"
                "{summary}\n\n"
                "New Code:\n"
                "{generated_code}\n\n"
                "Updated Summary:\n"
                "{updated_summary}\n"
            ),
        )

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=(
                "You are an expert machine learning code summarizer. Your role is to maintain an evolving, structured summary "
                "of an ML codebase by updating metadata and tracking long-lived variables.\n\n"
                "🧠 Each update must include:\n"
                "1. A brief **phase-level summary** of what the new code does (e.g., imputation, validation, EDA).\n"
                "2. An updated **flat list of all long-lived variables** created or modified (global or module-level scope).\n"
                "3. A `code_ref` indicating the function, class, or pipeline that governs this logic (e.g., `missing_analysis_pipeline()`).\n"
                "4. Optional `status`, `created_at`, and `task_type` metadata if this starts a new phase.\n\n"
                "✅ Include only variables that:\n"
                "- Exist after executing the code with `exec()`\n"
                "- Are assigned at the module level or persist in runtime memory\n"
                "- May be accessed or used by downstream components\n\n"
                "❌ Do NOT include:\n"
                "- Imported modules (`pd`, `np`, `SimpleImputer`, etc.)\n"
                "- Function parameters or loop/control variables (`i`, `col`, `row`, etc.)\n"
                "- In-line or short-lived comprehension/conditional variables\n"
                "- Any code, syntax, or explanation of code structure — just summarization and state\n"
            ),
            suffix=(
                "### YOUR TURN\n"
                "Previous Summary:\n"
                "{summary}\n\n"
                "New Code:\n"
                "{generated_code}\n\n"
                "Updated Summary:"
            ),
            input_variables=["summary", "generated_code"],
        )
