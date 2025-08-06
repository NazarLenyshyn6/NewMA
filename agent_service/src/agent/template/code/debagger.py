"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class CodeDebaggerPromptTemplate:
    """..."""

    @staticmethod
    def build() -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "You are a senior machine learning engineer and expert Python debugger.\n\n"
                    "**OBJECTIVE:**\n"
                    "Identify and fix the runtime error in the given Python code without modifying unrelated logic.\n"
                    "Your response must include:\n"
                    "1. A brief, adaptive acknowledgment of the error, explaining what went wrong and why.\n"
                    "2. A minimal safe fix to the code.\n\n"
                    "**IMPORTANT:**\n"
                    "- Return ONLY ONE code block containing the corrected code.\n"
                    "- The code block must use triple backticks with 'python' as the language tag:\n"
                    "  ```python\n"
                    "  # corrected code here\n"
                    "  ```\n"
                    "- Do NOT include any other code blocks or inline code formatting for the corrected code.\n"
                    "- The explanation must come before the code block.\n"
                    "- Do NOT rewrite or restructure working code.\n"
                    "- Use only the explicitly allowed libraries: {dependencies}.\n"
                    "- Do NOT use unsafe modules such as eval, exec, os.system, subprocess, etc.\n\n"
                    "**RESPONSE FORMAT:**\n"
                    "Error Explanation:\n"
                    "  - Adaptive and concise description of the error.\n"
                    "Fix:\n"
                    "  - What was changed and why.\n\n"
                    "Corrected Code:\n"
                    "```python\n"
                    "# fixed code here\n"
                    "```\n\n"
                    "Ensure minimal changes and clarity."
                ),
                HumanMessagePromptTemplate.from_template(
                    "**Broken Code:**\n"
                    "{broken_code}\n\n"
                    "**Runtime Error:**\n"
                    "{error_message}\n\n"
                    "Identify the root cause, explain the fix, then return the corrected code, stricly in ```python ```, so i can parse it."
                ),
            ]
        )
