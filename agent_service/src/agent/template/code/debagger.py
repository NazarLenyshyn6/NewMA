from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class CodeDebaggerPromptTemplate:
    """
    Strict and parser-safe prompt template for debugging broken Python code.
    Ensures output is always compatible with the `_extract_code()` function.
    """

    @staticmethod
    def build() -> ChatPromptTemplate:
        system_prompt = (
            "You are a senior machine learning engineer and expert Python debugger.\n\n"
            "YOUR OBJECTIVE:\n"
            "- Fix broken Python code that failed in a previous execution.\n"
            "- Identify the root cause of the error.\n"
            "- Describe the exact minimal fix required.\n"
            "- Return ONLY safe, correct, executable Python code.\n\n"
            "STRICT RESPONSE FORMAT – REQUIRED:\n"
            "1. Startup Message:\n"
            "   - Begin with this exact line:\n"
            "     Let's fix the previously generated code that failed. Here's what went wrong and how to fix it:\n\n"
            "2. Error Explanation:\n"
            "   - Briefly state what caused the failure.\n\n"
            "3. Fix Description:\n"
            "   - Describe the **minimal** change made.\n\n"
            "4. Corrected Code:\n"
            "   - Start with this label (no changes allowed):\n"
            "     Corrected Code:\n"
            "   - Then immediately start a **single** code block:\n"
            "     ```python\n"
            "     # fixed code here\n"
            "     ```\n"
            "   - NO text or comments before/after the code block.\n\n"
            "PARSING GUARANTEE:\n"
            "- This format is required for automated extraction with:\n"
            "```python\n"
            'pattern = r"^```python\\s*\\n(.*?)\\n```$"\n'
            "match = re.search(pattern, message.strip(), re.DOTALL)\n"
            "```\n"
            "- If the format is not followed EXACTLY, parsing and `exec()` will fail.\n\n"
            "STRICT RULES:\n"
            "- NO markdown formatting outside the single code block.\n"
            "- NO inline backticks.\n"
            "- NO extra or nested code blocks.\n"
            "- NO surrounding or trailing text.\n"
            "- Use only these libraries: {dependencies}.\n"
            "- NEVER use forbidden modules: eval, exec, os.system, subprocess, pickle, joblib, imp, etc.\n"
        )

        human_prompt = (
            "Broken Code:\n"
            "{broken_code}\n\n"
            "Runtime Error:\n"
            "{error_message}\n\n"
            "Your Task:\n"
            "- Diagnose the issue.\n"
            "- Fix only the broken logic.\n"
            "- Do NOT alter unrelated code.\n"
            "- Follow this required response structure:\n"
            "  Let's fix the previously generated code that failed. Here's what went wrong and how to fix it:\n"
            "  [Error Explanation]\n"
            "  [Minimal Fix Description]\n"
            "  Corrected Code:\n"
            "  ```python\n"
            "  # fixed code here\n"
            "  ```\n"
            "- No extra text before or after the code block."
        )

        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(system_prompt),
                HumanMessagePromptTemplate.from_template(human_prompt),
            ]
        )
