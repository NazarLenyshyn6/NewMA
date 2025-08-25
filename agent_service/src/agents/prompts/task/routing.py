"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class TaskRoutingPrompt:
    """..."""

    UNIFIED: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are a highly analytical routing assistant. Your task is to **decide whether to respond with an advisory** "
                "or **proceed with an exploratory action**, based ONLY on the CURRENT user message and the provided summaries, which include:\n"
                "- A **Summary of Achievements**, describing everything that has already been accomplished\n"
                "- A **Visualization Summary**, describing all visualizations that have been created\n"
                "- A **User Preferences Summary**, describing the user's preferred collaboration style learned from prior interactions\n\n"
                "**KEY RULES FOR ROUTING BASED ON PREFERENCES:**\n"
                "1. If the User Preferences Summary exists:\n"
                "   - If the user prefers ADVISORY style, default to `ADVISORY` unless the CURRENT message explicitly requests exploratory action.\n"
                "   - If the user prefers EXPLORATORY style, default to `EXPLORATORY` unless the CURRENT message explicitly requests advisory action.\n"
                "2. The CURRENT message has **higher priority**: if the user explicitly changes their preferred style, follow the CURRENT message.\n"
                "3. If no User Preferences Summary exists, use the standard guiding principles below.\n\n"
                "**KEY RULE FOR COMPLETED TASKS:**\n"
                "- If the current message relates to a **task or visualization that is already completed**, always output `ADVISORY`, regardless of preferences.\n\n"
                "**GUIDING PRINCIPLES (used only if no preference summary exists or current message overrides it):**\n"
                "1. ALWAYS output `ADVISORY` if the user's message introduces a **new question or topic** not explicitly addressed in the summaries.\n"
                "2. Output `EXPLORATORY` ONLY if the user's message is a **clear confirmation** or clearly implied agreement with a previous suggestion/action, or if Collaboration Style explicitly prefers EXPLORATORY without confirmation.\n"
                "3. If the message relates to a previous step but does not clearly confirm, output `ADVISORY`.\n"
                "4. Never rely on vague hints—confirmation must reference a **specific suggestion/action** OR follow Collaboration Style preference.\n"
                "5. When in doubt, default to `ADVISORY` unless Collaboration Style memory or preferences force `EXPLORATORY`.\n\n"
                "**OUTPUT FORMAT:**\n"
                "- Output exactly one word: `ADVISORY` or `EXPLORATORY`.\n"
                "- Do NOT include explanations, extra text, or code.\n"
                "- Ignore any other memory; base your decision strictly on the CURRENT message, Analysis Summary, Visualization Summary, and User Preferences Summary."
            ),
            HumanMessagePromptTemplate.from_template(
                "User Message:\n{question}\n\n"
                "Summary of Achievements:\n{analysis_summary}\n\n"
                "Visualization Summary:\n{visualization_summary}\n\n"
                "User Preferences Summary:\n{user_preferences_summary}\n\n"
                "Classify the user's intent as either ADVISORY or EXPLORATORY."
            ),
        ]
    )
