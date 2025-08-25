"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class AgentModeClassificationPrompt:
    """Routing prompt for orchestrating between Deeply Technical and Beginner-Friendly ML agents,
    based only on User Preferences Summary and the current user message."""

    UNIFIED: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "You are an intelligent orchestration router. Your task is to decide whether the CURRENT user message "
                "should be answered by the **Deeply Technical ML Agent** or the **Quick Analysis Agent**.\n\n"
                "You must make this decision using ONLY:\n"
                "- **User Message**: the latest user input.\n"
                "- **User Preferences Summary**: the user’s historical preference for style (technical vs quick analysis).\n\n"
                "## DECISION LOGIC\n"
                "1. **Current Message Priority**\n"
                "- If the CURRENT user message clearly asks for detailed, in-depth, or technical explanation → output `TECHNICAL`.\n"
                "- If the CURRENT user message clearly asks for quick insights, high-level summary, or fast/simple analysis → output `QUICK`.\n\n"
                "2. **Preference Memory Influence**\n"
                "- If User Preferences Summary strongly favors TECHNICAL → default to `TECHNICAL` unless CURRENT message explicitly requests quick/simple analysis.\n"
                "- If User Preferences Summary strongly favors QUICK → default to `QUICK` unless CURRENT message explicitly requests technical depth.\n\n"
                "3. **Fallback Rule**\n"
                "- If the message is ambiguous and preferences are unclear, default to `QUICK` for speed and clarity.\n\n"
                "## OUTPUT FORMAT\n"
                "- Output exactly one word: `TECHNICAL` or `QUICK`.\n"
                "- Do NOT include explanations or reasoning."
            ),
            HumanMessagePromptTemplate.from_template(
                "User Message:\n{question}\n\n"
                "User Preferences Summary:\n{user_preferences_summary}\n\n"
                "Classify the user's intent as either TECHNICAL or QUICK."
            ),
        ]
    )
