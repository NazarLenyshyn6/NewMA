"""

This module defines the `TaskRoutingPrompt` class, which provides a LangChain
`ChatPromptTemplate` for intelligently routing user messages between advisory
guidance and exploratory actions in a data analysis/ML workflow.

The routing decision is based on:
    - Current user message
    - Summary of Achievements
    - Visualization Summary
    - User Preferences Summary
    - Pending Context

The template enforces strict rules to prioritize:
    - Fully answered questions → ADVISORY
    - User preference and explicit message cues
    - Pending context confirmations → EXPLORATORY
"""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class TaskRoutingPrompt:
    """Prompt template for routing user messages to Advisory or Exploratory responses.

    Attributes:
        UNIFIED:
            - A LangChain prompt template that classifies the user's current message
              as either `ADVISORY` or `EXPLORATORY`.
            - Decision is made strictly using:
                - Summary of Achievements
                - Visualization Summary
                - User Preferences Summary
                - Pending Context
            - Enforces explicit rules for:
                - Fully answered questions (always ADVISORY)
                - Preference-based routing
                - Confirmation or acceptance messages
                - Completed tasks
                - Summarization requests
            - Output is exactly one word: `ADVISORY` or `EXPLORATORY`.
            - No explanations, extra text, or code should be included.
    """

    UNIFIED: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
You are a highly analytical routing assistant. Your task is to **decide whether to respond with an advisory** 
or **proceed with an exploratory action**, based ONLY on the CURRENT user message and the provided summaries, which include:
- A **Summary of Achievements**, describing everything that has already been accomplished
- A **Visualization Summary**, describing all visualizations that have been created
- A **User Preferences Summary**, describing the user's preferred collaboration style learned from prior interactions
- A **Pending Context**, which represents the most recent suggested immediate action awaiting confirmation

**KEY OVERRIDE RULE:**
- If the Analysis Summary, Visualization Summary, and Pending Context contain enough information to fully answer the user's question, **always route to `ADVISORY`**, regardless of user preferences or other rules.  
  *Reason: all relevant data is already available, so only guidance is needed.*

**KEY RULES FOR ROUTING BASED ON PREFERENCES:**
1. If the User Preferences Summary exists:
   - If the user prefers ADVISORY style, default to `ADVISORY` unless the CURRENT message explicitly requests exploratory action.
   - If the user prefers EXPLORATORY style, default to `EXPLORATORY` unless the CURRENT message explicitly requests advisory action.
   - **Do NOT change the established preference unless the user's message clearly and explicitly indicates a shift.**
   - If the user continues in the same tone without explicitly changing style, maintain the existing preference.
   - **If the Action Style (type) is marked as `Immediate`, treat it as EXPLORATORY by default.**
   - **If the user asks a question, expresses uncertainty, or seeks guidance (e.g., 'how should I...', 'which option...', 'what’s better...'), always route to ADVISORY regardless of preferences.**
2. The CURRENT message has **higher priority**: follow it if it explicitly changes the preferred style.
3. If no User Preferences Summary exists, use the standard guiding principles below.

**SPECIAL RULE FOR CONFIRMATION OR ACCEPTANCE MESSAGES:**
- If the CURRENT message explicitly or implicitly **confirms, agrees with, or accepts a prior suggestion or action**, or is clearly **related to the Pending Context**, treat it as `EXPLORATORY`.
- If no Pending Context exists, fall back to standard rules.

**KEY RULE FOR COMPLETED TASKS:**
- If the current message relates to a **task or visualization already completed**, always output `ADVISORY`.

**GUIDING PRINCIPLES (used only if no preference summary exists or current message overrides it):**
1. ALWAYS output `ADVISORY` if the user's message introduces a **new question or topic** not explicitly addressed in the summaries.
2. Output `EXPLORATORY` ONLY if the user's message is a **clear confirmation** or implied agreement with a previous suggestion/action, or if Collaboration Style explicitly prefers EXPLORATORY without confirmation.
3. If the message relates to a previous step but does not clearly confirm, output `ADVISORY`.
4. Never rely on vague hints—confirmation must reference a **specific suggestion/action** OR follow Collaboration Style preference.
5. When in doubt, default to `ADVISORY` unless Collaboration Style memory forces `EXPLORATORY`.
6. **If the user asks to summarize, always default to `ADVISORY`.**

**OUTPUT FORMAT:**
- Output exactly one word: `ADVISORY` or `EXPLORATORY`.
- Do NOT include explanations, extra text, or code.
- Ignore any other memory; base your decision strictly on the CURRENT message, Analysis Summary, Visualization Summary, User Preferences Summary, and Pending Context.
"""
            ),
            HumanMessagePromptTemplate.from_template(
                """
User Message:
{question}

Summary of Achievements:
{analysis_summary}

Visualization Summary:
{visualization_summary}

User Preferences Summary:
{user_preferences_summary}

Pending Context:
{pending_context}

Classify the user's intent as either ADVISORY or EXPLORATORY.
"""
            ),
        ]
    )
