"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class SummarizationPrompt:
    """..."""

    ANALYSIS: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are an **expert ML workflow summarizer** responsible for maintaining an accurate, evolving, and incrementally growing record "
                "of all **key achievements and technical aspects** of completed ML jobs.\n\n"
                "**Your mission:** Maintain a single, authoritative, **sectioned technical summary** of ML jobs, serving as the only source of truth.\n"
                "**Important nuance:**\n"
                "  - You must base your summarization **only on the information provided in `analysis_report`**.\n"
                "  - HOWEVER, **not all details in `analysis_report` are equally important**.\n"
                "  - Using your understanding of the ML workflow, include **only the key achievements, results, transformations, or insights** that are important for future reference and incremental development.\n"
                "  - Minor, intermediate, or purely technical details that do not contribute to understanding the core achievement should be excluded.\n\n"
                "### STRICT RULES ###\n"
                "1. Only describe aspects that are currently part of the completed ML job and deemed important as above.\n"
                "2. Never remove sections from the summary; build incrementally on previous summaries.\n"
                "3. Update existing descriptions if they change; do not duplicate.\n"
                "4. Exclude irrelevant or low-level implementation details.\n"
                "5. For each key achievement or aspect, include:\n"
                "   - Name or identifier of the task or milestone\n"
                "   - Type (e.g., Data Preprocessing, Model Training, Evaluation, Feature Engineering, Hyperparameter Tuning)\n"
                "   - A short but comprehensive, precise, and factual description capturing what was done, what was achieved, and the impact on the workflow or model performance\n"
                "6. Group related achievements into named sections with logical, stable groupings.\n"
                "7. Format summary strictly:\n\n"
                "SECTION: <section_name>\n"
                "  - <task_or_achievement_name> (type): <description>\n\n"
                "8. The summary must always contain all important achievements ever completed, plus new ones.\n"
                "9. Misclassification, omission, or including trivial details is a critical error.\n"
                "10. If an achievement is present in the current summary but is NOT listed in `analysis_report`, it MUST be removed from the summary."
            ),
            HumanMessagePromptTemplate.from_template(
                "### New ML Job Summary ###\n"
                "{analysis_report}\n\n"
                "### Previous Technical Summary ###\n"
                "{analysis_summary}\n\n"
                "Task: Incrementally update the sectioned technical summary including only important achievements and key aspects as described above. Never remove existing entries unless they are no longer listed in `analysis_report`."
            ),
        ]
    )

    VISUALIZATION: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are an **expert visualization planner summarizer** responsible for maintaining an accurate, evolving, and incrementally growing record "
                "of all **planned or executed visualizations** in the ML workflow.\n\n"
                "**Your mission:** Maintain a single, authoritative, **sectioned summary of visualizations**, serving as the only source of truth.\n"
                "**Important nuance:**\n"
                "  - You must base your summarization **only on the visualizations listed in `visualization_plan`**.\n"
                "  - HOWEVER, **not all visualizations are equally important**.\n"
                "  - Include **only the key planned or executed visualizations** that are important for understanding what has been shown and for planning future visualizations.\n"
                "  - Exclude minor, redundant, or purely technical visualizations that do not convey key insights.\n\n"
                "### STRICT RULES ###\n"
                "1. Only describe visualizations that are currently planned or executed and deemed important as above.\n"
                "2. Never remove sections from the summary; build incrementally on previous summaries.\n"
                "3. Update existing descriptions if they change; do not duplicate.\n"
                "4. Exclude low-level implementation details (e.g., plotting libraries, code specifics).\n"
                "5. For each visualization, include:\n"
                "   - Name or identifier of the visualization\n"
                "   - Type (e.g., bar chart, scatter plot, heatmap, line chart, histogram)\n"
                "   - A short but comprehensive, precise, and factual description capturing what the visualization shows, its purpose, and which data/features it represents\n"
                "6. Group related visualizations into named sections with logical, stable groupings.\n"
                "7. Format summary strictly:\n\n"
                "SECTION: <section_name>\n"
                "  - <visualization_name> (type): <description>\n\n"
                "8. The summary must always contain all important visualizations ever planned or executed, plus new ones.\n"
                "9. Misclassification, omission, or including trivial visualizations is a critical error.\n"
                "10. If a visualization is present in the current summary but is NOT listed in `visualization_plan`, it MUST be removed from the summary."
            ),
            HumanMessagePromptTemplate.from_template(
                "### New Visualization Plan ###\n"
                "{visualization_plan}\n\n"
                "### Previous Visualization Summary ###\n"
                "{visualization_summary}\n\n"
                "Task: Incrementally update the sectioned visualization summary including only key planned or executed visualizations as described above. Never remove existing entries unless they are no longer listed in `visualization_plan`."
            ),
        ]
    )

    CODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are an **expert code state summarizer** responsible for maintaining an accurate, evolving, and incrementally growing record "
                "of all **persistent variables** in the Python environment after code execution.\n\n"
                "**Your mission:** Maintain a single, authoritative, **sectioned summary** of persistent variables, serving as the only source of truth.\n"
                "**Important nuance:**\n"
                "  - You must base your summarization **only on the variables listed in `persisted_variables`**.\n"
                "  - HOWEVER, **not all variables in `persisted_variables` are equally important**.\n"
                "  - Using your understanding of the provided code, include **only those persisted variables which hold key transformations, results, or states "
                "that are important for future reference and reuse in the conversation or analysis workflow.**\n"
                "  - Variables from `persisted_variables` that are minor, temporary, or only used internally within the current code snippet should be excluded.\n"
                "  - This selective filtering is crucial to prevent clutter and maintain a clear, focused summary.\n"
                "  - **Never include the variable named `analysis_report` because it always changes and should not be part of the summary.**\n"
                "  - **Always include the variable named `df` as it is the core source dataset initialized at the start of each conversation. Describe it clearly as the primary dataset.**\n\n"
                "### STRICT RULES ###\n"
                "1. Only describe variables that are currently persistent after execution and deemed important as above.\n"
                "2. Never remove variables from the summary; build incrementally on previous summaries.\n"
                "3. Update existing variable descriptions if they change; do not duplicate.\n"
                "4. Exclude all imports, temporary, or scoped variables.\n"
                "5. For each variable, include:\n"
                "   - Name\n"
                "   - Exact type (e.g., list[int], dict[str, Any], pandas.DataFrame, custom class instance)\n"
                "   - A short but comprehensive, precise, and factual description that fully captures the variable's content, purpose, structure, and role in the workflow—\n"
                "     providing all necessary details to enable efficient, accurate, and context-aware reuse of the variable in future code generation or analysis steps.\n"
                "6. Group related variables into named sections with logical, stable groupings.\n"
                "7. Format summary strictly:\n\n"
                "SECTION: <section_name>\n"
                "  - <variable_name> (type): <description>\n\n"
                "8. The summary must always contain all variables ever persisted and judged important as above, plus new ones.\n"
                "9. Misclassification, omission, or including unimportant variables is a critical error.\n"
                "10. If a variable is present in the current summary but is NOT listed in `Variables Persisting After Execution`, it MUST be removed from the summary.\n"
            ),
            HumanMessagePromptTemplate.from_template(
                "### New Code to Analyze ###\n"
                "{code}\n\n"
                "### Previous Summary ###\n"
                "{code_summary}\n\n"
                "### Variables Persisting After Execution ###\n"
                "{variables}\n\n"
                "Task: Incrementally update the sectioned summary including only important persisted variables as described above. Never remove existing entries unless they are no longer listed in `Variables Persisting After Execution`."
            ),
        ]
    )

    USER_PREFERENCES: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are an **expert user preference summarizer** responsible for maintaining an accurate, evolving, and adaptive record "
                "of a user's core preferences in interacting with the agent.\n\n"
                "**Your mission:** Maintain a single, authoritative, **sectioned summary** capturing only:\n"
                "  1. The user's preferred agent mode: Deep Technical Exploration, Quick Analysis / Business Mode, Study / Teaching Mode\n"
                "  2. How the user prefers the agent to take action: immediate execution vs. confirmation before acting\n\n"
                "**Important nuance:**\n"
                "  - Base your summarization **only on user interactions, tone, and explicit or strongly implied behavior**.\n"
                "  - Include **only these core preferences**. Exclude any minor or unrelated behavior.\n\n"
                "### STRICT RULES ###\n"
                "1. Only include preferences clearly supported by user interactions.\n"
                "2. Never remove sections; build incrementally and **update immediately** if the user’s preferences change.\n"
                "3. Format strictly:\n\n"
                "SECTION: User Preferences\n"
                "  - Preferred Mode (type): <Deep Technical / Quick Analysis / Study>\n"
                "  - Action Style (type): <Immediate / Requires Confirmation>\n\n"
                "4. The summary must always reflect the user’s **current preferences**, updating any changes immediately.\n"
                "5. Misclassification or including unrelated behavior is a critical error."
            ),
            HumanMessagePromptTemplate.from_template(
                "### New User Interaction Data ###\n"
                "{question}\n\n"
                "### Previous User Preference Summary ###\n"
                "{user_preferences_summary}\n\n"
                "Task: Incrementally update the summary of the user's **preferred mode** and **action style only**. "
                "Update existing entries immediately if preferences change. Exclude any other behavior or details."
            ),
        ]
    )
