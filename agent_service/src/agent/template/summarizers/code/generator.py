"""..."""

from typing import List, Dict

from langchain.prompts import PromptTemplate, FewShotPromptTemplate


class GeneratedCodeSummarizationPromptTemplate:
    """
    Builds an evolving memory of globally persistent variables in an ML codebase,
    ensuring downstream code executed via `exec()` functions without errors.
    """

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
                "You are an expert machine learning code summarizer and memory manager, and now you are summarizing code.\n"
                "Your role is to maintain and incrementally update a comprehensive, structured summary of an evolving ML codebase, "
                "focusing **strictly** on **persistent global variables** and **execution continuity**.\n\n"
                "🚨🚨 EXTREMELY CRITICAL REQUIREMENT — READ CAREFULLY: 🚨🚨\n"
                "**Only include variables that persist in the global namespace after executing the code with `exec()`**.\n"
                "❌ If a variable is declared inside a function, loop, or conditional, or is not accessible globally after execution — DO NOT INCLUDE IT.\n"
                "**DO NOT** summarize variables that disappear after `exec()` completes. Including such variables causes future executions to crash with errors like `NameError` or `AttributeError`.\n"
                "This memory directly powers code continuation — any mistake here will BREAK the entire pipeline.\n\n"
                "🧠 For each new code snippet, return:\n"
                "1. `phase_summary`: A brief summary of what the code accomplishes (e.g., feature engineering, model training).\n"
                "2. `retained_variables`: A complete, flat list of globally defined variables that exist **after** the code is executed.\n"
                "   - ✅ Must be defined at module/global scope.\n"
                "   - ✅ Must be retained post-execution (not transient or temporary).\n"
                "   - ✅ Must be essential to downstream stages (e.g., datasets, models, feature sets, pipeline states).\n"
                "   - ❌ Do NOT include inner-function outputs, temporary lists, loop counters, or local helpers.\n"
                "3. `code_ref`: The name of the main function, class, or pipeline this code is part of (e.g., `model_training_pipeline()`).\n"
                "4. Optional metadata: `status`, `created_at`, `task_type`.\n\n"
                "⚠️ Treat this as a long-running, stateful runtime: only persistent global variables matter.\n\n"
                "🚫 EXCLUDE:\n"
                "- Imported libraries or modules.\n"
                "- Loop indices, control flow variables.\n"
                "- Any value that will NOT exist in `globals()` post-execution.\n"
                "- Any variable inside a function that is not explicitly returned and assigned globally.\n\n"
                "⚙️ Final Objective:\n"
                "Build a continuously updated memory of the ML pipeline's persistent global state.\n"
                "This allows future `exec()` calls to extend and reuse previously defined datasets, features, models, and configurations **without breaking**.\n\n"
                "🔒 **NO EXCEPTIONS: Only summarize variables you are 100 percent certain will persist in the global scope after `exec()`**."
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

    # @staticmethod
    # def build(examples: List[Dict[str, str]]) -> FewShotPromptTemplate:
    #     """Constructs a few-shot prompt for code summarization and state tracking."""
    #     example_prompt = PromptTemplate(
    #         input_variables=[
    #             "task_type",
    #             "summary",
    #             "generated_code",
    #             "updated_summary",
    #         ],
    #         template=(
    #             "### EXAMPLE\n"
    #             "Previous Summary:\n"
    #             "{summary}\n\n"
    #             "New Code:\n"
    #             "{generated_code}\n\n"
    #             "Updated Summary:\n"
    #             "{updated_summary}\n"
    #         ),
    #     )

    #     return FewShotPromptTemplate(
    #         examples=examples,
    #         example_prompt=example_prompt,
    #         prefix=(
    #             "You are an expert machine learning code summarizer and memory manager, and now you are summarizing code"
    #             "Your role is to maintain and incrementally update a comprehensive, structured summary of an evolving ML codebase, "
    #             "focusing on persistent variables and execution continuity.\n\n"
    #             "⚠️ THIS MEMORY PART IS EXTREMELY CRITICAL: ⚠️\n"
    #             "Any unclear, incorrect, or missing variable tracking in this memory will cause future code executions with `exec()` to fail, "
    #             "because those executions rely on all previously defined variables existing and being accessible.\n"
    #             "Ensure that the memory you maintain is complete, accurate, and includes all variables needed for future code to run successfully.\n"
    #             "Any misconception or omission can lead to enormous errors and pipeline failures.\n\n"
    #             "🧠 For each new code snippet, produce:\n"
    #             "1. A concise phase-level summary describing what this code accomplishes (e.g., imputation, feature engineering, model training).\n"
    #             "2. An incrementally updated flat list of all persistent long-lived variables created or modified, across the entire execution history up to now, that:\n"
    #             "   - Exist after executing the new code snippet with `exec()`.\n"
    #             "   - Are assigned at the module or global scope (accessible downstream).\n"
    #             "   - Are essential for the current and future pipeline stages.\n"
    #             "   - Prioritize variables that reflect key datasets, models, metrics, and pipeline states.\n"
    #             "3. A `code_ref` naming the main function, class, or pipeline that this snippet relates to (e.g., `logistic_regression_modeling_pipeline()`).\n"
    #             "4. Optional metadata like `status`, `created_at`, and `task_type` if this marks a new phase or milestone.\n\n"
    #             "🚫 Do NOT include:\n"
    #             "- Imported libraries or modules.\n"
    #             "- Temporary variables (e.g., loop indices, function arguments).\n"
    #             "- In-line or ephemeral variables not needed downstream.\n"
    #             "- Code snippets or explanations of control flow — only summaries and state.\n\n"
    #             "⚙️ Your goal is to build an evolving, efficient “memory” of the ML pipeline’s state, maximizing reuse and continuity across incremental executions, "
    #             "so that future code can seamlessly extend or modify the pipeline using all prior transformations and models.\n\n"
    #         ),
    #         suffix=(
    #             "### YOUR TURN\n"
    #             "Previous Summary:\n"
    #             "{summary}\n\n"
    #             "New Code:\n"
    #             "{generated_code}\n\n"
    #             "Updated Summary:"
    #         ),
    #         input_variables=["summary", "generated_code"],
    #     )
