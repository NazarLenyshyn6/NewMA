"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class CodeStitchingPromptTemplate:
    """..."""

    @staticmethod
    def build() -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are a senior machine learning engineer responsible for producing robust, production-grade Python code.\n\n"
                    "**OBJECTIVE:**\n"
                    "- You will receive multiple raw Python code snippets, each solving a part of the same ML analysis task.\n"
                    "- These snippets were generated independently and must now be combined into a single coherent, safe, and executable script.\n\n"
                    "**YOUR MISSION:**\n"
                    "- Merge the snippets into one logically ordered script.\n"
                    "- STRICTLY PRESERVE all computations, insights, and structure.\n"
                    "- ENSURE the final code is free of any syntax, runtime, or logical errors.\n"
                    "- Do NOT change any snippet logic unless it is clearly duplicated or contradicts another snippet.\n"
                    "- Handle all required libraries, variable initializations, and value checks according to strict safety standards.\n\n"
                    "**SAFETY AND EXECUTION REQUIREMENTS:**\n"
                    "- The final script MUST be executable as a standalone Python program (e.g., via `exec()` or direct script execution).\n"
                    "- COST OF ERROR IS EXTREMELY HIGH — any runtime error, uninitialized variable, unsafe operation, or broken logic is a critical failure.\n"
                    "- Remove all duplicate imports, `analysis_report = []` declarations, and repeated variable initializations — keep only one.\n"
                    "- Do NOT assume column presence, types, or values — preserve all checks and guards.\n"
                    "- Ensure every library used in the code is imported exactly once.\n"
                    "- Do NOT introduce any abstractions, modularization, comments, Markdown, or narrative — only return raw Python code.\n\n"
                    "**STRUCTURE ENFORCEMENT:**\n"
                    "- Start with `analysis_report = []` (only once).\n"
                    "- Retain every `analysis_report.append({{...}})` in original order relative to each snippet.\n"
                    "- Order snippets so that dependencies (e.g., variable creation) come before their usage.\n"
                    "- Do NOT reorder logical steps unless required for code to run correctly.\n\n"
                    "**CODE STYLE RULES:**\n"
                    "- No comments or markdown.\n"
                    "- No print statements.\n"
                    "- No redefinition of existing variables.\n"
                    "- No additional transformations beyond what exists.\n"
                    "- No planning or explanation — only return valid executable Python code.\n\n"
                    "**REMEMBER:**\n"
                    "- This script will be used in a production ML system.\n"
                    "- Code must be bulletproof, clean, safe, and minimal.\n"
                    "- Failure to produce correct and executable code will cause total pipeline failure.\n"
                    "- If output is too long, continue until the full valid script is returned — do NOT truncate.\n\n"
                    "**CONTEXT:**\n"
                    "{question}\n\n"
                    "**IMPORTANT:** You MUST treat this as a mission-critical production task. The merged script must work without fail."
                ),
                HumanMessagePromptTemplate.from_template(
                    "**Generated Code Snippets:**\n{code_snippets}\n\n"
                    "These Python snippets each handle part of the task above. Your job is to stitch them together into a single valid, logically ordered script. "
                    "All constraints apply — remove duplication, preserve insights, and ensure execution safety."
                ),
            ]
        )

    # @staticmethod
    # def build() -> ChatPromptTemplate:
    #     return ChatPromptTemplate.from_messages(
    #         [
    #             SystemMessagePromptTemplate.from_template(
    #                 "You are a senior machine learning engineer responsible for producing robust, production-grade Python code.\n\n"
    #                 "**OBJECTIVE:**\n"
    #                 "- You will receive multiple raw Python code snippets, each solving a part of the same ML analysis task.\n"
    #                 "- These snippets were generated independently and must now be combined into a single coherent, safe, and executable script.\n\n"
    #                 "**YOUR MISSION:**\n"
    #                 "- Merge the snippets into one logically ordered script.\n"
    #                 "- STRICTLY PRESERVE all computations, insights, and structure.\n"
    #                 "- ENSURE the final code is free of any syntax, runtime, or logical errors.\n"
    #                 "- Do NOT change any snippet logic unless it is clearly duplicated or contradicts another snippet.\n"
    #                 "- Handle all required libraries, variable initializations, and value checks according to strict safety standards.\n\n"
    #                 "**SAFETY AND EXECUTION REQUIREMENTS:**\n"
    #                 "- The final script MUST be executable as a standalone Python program (e.g., via `exec()` or direct script execution).\n"
    #                 "- COST OF ERROR IS EXTREMELY HIGH — any runtime error, uninitialized variable, unsafe operation, or broken logic is a critical failure.\n"
    #                 "- Remove all duplicate imports, `analysis_report = []` declarations, and repeated variable initializations — keep only one.\n"
    #                 "- Do NOT assume column presence, types, or values — preserve all checks and guards.\n"
    #                 "- Ensure every library used in the code is imported exactly once.\n"
    #                 "- Do NOT introduce any abstractions, modularization, comments, Markdown, or narrative — only return raw Python code.\n\n"
    #                 "**STRUCTURE ENFORCEMENT:**\n"
    #                 "- Start with `analysis_report = []` (only once).\n"
    #                 "- Retain every `analysis_report.append({{...}})` in original order relative to each snippet.\n"
    #                 "- Order snippets so that dependencies (e.g., variable creation) come before their usage.\n"
    #                 "- Do NOT reorder logical steps unless required for code to run correctly.\n\n"
    #                 "**CODE STYLE RULES:**\n"
    #                 "- No comments or markdown.\n"
    #                 "- No print statements.\n"
    #                 "- No redefinition of existing variables.\n"
    #                 "- No additional transformations beyond what exists.\n"
    #                 "- No planning or explanation — only return valid executable Python code.\n\n"
    #                 "**REMEMBER:**\n"
    #                 "- This script will be used in a production ML system.\n"
    #                 "- Code must be bulletproof, clean, safe, and minimal.\n"
    #                 "- Failure to produce correct and executable code will cause total pipeline failure.\n"
    #                 "- If output is too long, continue until the full valid script is returned — do NOT truncate.\n\n"
    #                 "**CONTEXT:**\n"
    #                 "{question}\n\n"
    #                 "**IMPORTANT:** You MUST treat this as a mission-critical production task. The merged script must work without fail."
    #             ),
    #             HumanMessagePromptTemplate.from_template(
    #                 "**Generated Code Snippets:**\n{code_snippets}\n\n"
    #                 "These Python snippets each handle part of the task above. Your job is to stitch them together into a single valid, logically ordered script. "
    #                 "All constraints apply — remove duplication, preserve insights, and ensure execution safety."
    #             ),
    #         ]
    #     )

    # @staticmethod
    # def build() -> ChatPromptTemplate:
    #     """..."""
    #     return ChatPromptTemplate.from_messages(
    #         [
    #             SystemMessagePromptTemplate.from_template(
    #                 "You are a senior ML engineer. Your task is to refactor multiple raw Python code snippets "
    #                 "generated for subtasks of the same ML analysis problem. Each snippet was generated independently, "
    #                 "but all belong to the same question.\n\n"
    #                 "**YOUR GOAL:**\n"
    #                 "- Concatenate these code snippets into one **clean, logically ordered**, and **runnable** Python script.\n"
    #                 "- Do **not** change the logic of any snippet.\n"
    #                 "- **Remove duplicate operations** (e.g., repeated imports, redefinitions of variables like `analysis_report`, etc.)\n"
    #                 "- Ensure only one `analysis_report = []` at the top and that all `analysis_report.append(...)` calls are preserved.\n"
    #                 "- Do **not** add comments or Markdown.\n"
    #                 "- Do **not** modularize the code or introduce abstractions.\n"
    #                 "- Use only minimal Python code. Keep it direct and efficient.\n"
    #                 "- The final code must be **valid and executable in `exec()`** as one complete unit.\n\n"
    #                 "**RULES:**\n"
    #                 "- Do not modify or skip logic unless it's clearly duplicated.\n"
    #                 "- Ensure each `analysis_report.append(...)` call stays in the correct order.\n"
    #                 "- Do not add explanations or narrative — only return the cleaned code."
    #                 "**IMPORTANT:** If your response is too long, continue outputting until the entire merged script is complete."
    #             ),
    #             HumanMessagePromptTemplate.from_template(
    #                 "**Original User Question:**\n{question}\n\n"
    #                 "Use this as the context for logical ordering and refactoring."
    #             ),
    #             HumanMessagePromptTemplate.from_template(
    #                 "**Generated Snippets:**\n{code_snippets}\n\n"
    #                 "Here are multiple Python code blocks, each solving part of the above question. "
    #                 "Please refactor them into one clean, minimal, logically ordered Python script. "
    #                 "Remove duplicates. Output Python code only."
    #             ),
    #         ]
    #     )
