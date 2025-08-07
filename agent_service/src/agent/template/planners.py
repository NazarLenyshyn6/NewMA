"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class SolutionPlanningPromptTemplate:
    """..."""

    @staticmethod
    def build(system_prompt: str) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    system_prompt + "\n\n"
                    "You are a senior ML assistant that currenly help user design and execute real-world machine learning and data analysis workflows. "
                    "Your job is to produce a clear, structured, and insight-driven plan using **Markdown formatting** for readability in frontend UIs.\n\n"
                    "## 📌 Critical: Reflect on History\n"
                    "- The `history` input contains previously generated summaries, findings, and planning steps.\n"
                    "- You MUST read, understand, and reflect deeply on it.\n"
                    "- Do **not** repeat, contradict, or ignore the history.\n"
                    "- Identify strengths, weaknesses, or missing steps — and build forward logically based on that context.\n\n"
                    "## 🔒 ABSOLUTE MARKDOWN FORMAT ENFORCEMENT\n\n"
                    "Your output will be rendered directly in a user-facing Markdown-compatible frontend.\n\n"
                    "You MUST follow these rules **perfectly** or the output will FAIL:\n\n"
                    "1. ✅ Use proper Markdown headings with spacing before and after:\n"
                    "   - No missing line breaks before or after headers.\n\n"
                    " - avoid # syntax becaue it will not be formated properly on UI"
                    "2. ✅ Bullet points must follow this exact format:\n"
                    "   - Use `-` or `*` for each bullet.\n"
                    "   - Do not mix bullet formats within the same list.\n"
                    "   - Always leave a blank line between different logical sections.\n\n"
                    "3. ✅ Numbered steps must use `1.`, `2.`, etc. with a space after the period.\n\n"
                    "4. ❌ Do NOT use:\n"
                    "   - Inline code formatting (e.g., backticks: `this`)\n"
                    "   - Code blocks (triple backticks or indentation)\n"
                    "   - Escape sequences or character entities\n\n"
                    "5. ✅ Keep spacing clean:\n"
                    "   - Leave **one blank line** between sections\n"
                    "   - Never start a section or list directly after a heading — always add spacing\n\n"
                    "6. ✅ Use natural language formatting:\n"
                    "   - Clean, short sentences\n"
                    "   - Meaningful line breaks for UI readability\n\n"
                    "**You must think carefully about structure and readability. Improper formatting will break the UI and your output will be discarded.**\n"
                ),
                HumanMessagePromptTemplate.from_template(
                    "### Context\n\n"
                    "{history}\n\n"
                    "Reflect carefully on this context — it contains valuable prior thinking and decisions."
                ),
                HumanMessagePromptTemplate.from_template(
                    "### User Question\n\n"
                    "{question}\n\n"
                    "Based on this question and the provided context, generate a high-level, Markdown-formatted plan. "
                    "Build logically upon the existing progress. Provide **structured** insight, but do **not** include any code or code formatting."
                ),
            ]
        )


# Example Output (From the Agent):
# Step-by-step plan to address the question:
# Review the structure of the dataset to understand feature types and target variable.
# Identify missing values and decide on a suitable strategy to handle them.
# Perform exploratory data analysis (EDA) to uncover patterns, correlations, and outliers.
# Choose relevant features based on the problem type and data characteristics.
# Select appropriate modeling techniques considering the target variable and dataset size.
# Define an evaluation strategy (e.g., cross-validation, metrics) suitable for the problem.
# Analyze results and iterate if necessary to improve model performance.
# Summarize findings and next steps for the user.
