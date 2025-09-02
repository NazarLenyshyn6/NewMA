"""

This module defines the `AgentModeClassificationPrompt` class, which provides
a LangChain `ChatPromptTemplate` for routing user queries between different
agents based on **user preferences** and the **current message context**.

Specifically, the prompt ensures that user questions are directed either to:
    - The **Deeply Technical ML Agent** → for detailed, rigorous, FAANG-level
      technical reasoning and explanations.
    - The **Quick Analysis Agent** → for high-level, concise, beginner-friendly
      insights and summaries.

The classification relies exclusively on:
    - The latest **user message**.
    - The **User Preferences Summary**, which tracks whether the user tends to
      prefer detailed technical explanations or quick/simple analyses.

This routing ensures that responses are always aligned with both **current
intent** and **historical preference**.
"""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class AgentModeClassificationPrompt:
    """Routing prompt for deciding whether to use a technical or quick-response agent.

    The `AgentModeClassificationPrompt` is responsible for **classifying the
    mode of response** for the user’s current message. It chooses between:

        - `TECHNICAL`: If the message requires in-depth reasoning,
          advanced explanations, or matches the user’s historical preference
          for technical detail.

        - `QUICK`: If the message requests short, simple, high-level insights,
          or matches the user’s historical preference for quick analysis.

    Decision logic is based on:
        1. **Current Message Priority**:
           - Direct user request for technical depth → `TECHNICAL`.
           - Direct user request for simplicity/speed → `QUICK`.

        2. **Preference Memory Influence**:
           - If the preference summary strongly favors one mode, default to it,
             unless the current message explicitly requests the opposite.

        3. **Fallback Rule**:
           - If ambiguous or unclear, default to `QUICK`.

    Attributes:
        UNIFIED (ChatPromptTemplate):
            A composite LangChain prompt with:
                - System instructions:
                    Defines strict classification rules for routing.
                - Human message template:
                    Provides the user’s latest question and the summarized
                    preferences for decision-making.

            Output:
                - Always a single word: `TECHNICAL` or `QUICK`.
                - No reasoning, explanations, or extra formatting.

    """

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
                "- If User Preferences Summary strongly favors QUICK → default to `QUICK` unless CURRENT message explicitly requests technical depth.\n"
                "- **Do NOT change the established preference summary unless the user’s message clearly and explicitly indicates a shift in preference.**\n"
                "- If the user continues their interaction without explicitly changing style (e.g., just extending discussion in the same tone), maintain the existing preference.\n\n"
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
