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
        """..."""
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are a senior ML engineer. Your task is to refactor multiple raw Python code snippets "
                    "generated for subtasks of the same ML analysis problem. Each snippet was generated independently, "
                    "but all belong to the same question.\n\n"
                    "**YOUR GOAL:**\n"
                    "- Concatenate these code snippets into one **clean, logically ordered**, and **runnable** Python script.\n"
                    "- Do **not** change the logic of any snippet.\n"
                    "- **Remove duplicate operations** (e.g., repeated imports, redefinitions of variables like `analysis_report`, etc.)\n"
                    "- Ensure only one `analysis_report = []` at the top and that all `analysis_report.append(...)` calls are preserved.\n"
                    "- Do **not** add comments or Markdown.\n"
                    "- Do **not** modularize the code or introduce abstractions.\n"
                    "- Use only minimal Python code. Keep it direct and efficient.\n"
                    "- The final code must be **valid and executable in `exec()`** as one complete unit.\n\n"
                    "**RULES:**\n"
                    "- Do not modify or skip logic unless it's clearly duplicated.\n"
                    "- Ensure each `analysis_report.append(...)` call stays in the correct order.\n"
                    "- Do not add explanations or narrative — only return the cleaned code."
                    "**IMPORTANT:** If your response is too long, continue outputting until the entire merged script is complete."
                ),
                HumanMessagePromptTemplate.from_template(
                    "**Original User Question:**\n{question}\n\n"
                    "Use this as the context for logical ordering and refactoring."
                ),
                HumanMessagePromptTemplate.from_template(
                    "**Generated Snippets:**\n{code_snippets}\n\n"
                    "Here are multiple Python code blocks, each solving part of the above question. "
                    "Please refactor them into one clean, minimal, logically ordered Python script. "
                    "Remove duplicates. Output Python code only."
                ),
            ]
        )
