"""
This module defines the `SubtaskClassificationPrompt` class, which provides a
LangChain `ChatPromptTemplate` for classifying user questions into one of three
strict response modes: analysis, visualization, or direct response.

The classification is based on:
    - Prior analysis summaries
    - Visualization summaries
    - Pending context (the most recent suggested immediate action)

The unified prompt enforces strict decision rules to ensure consistent,
unambiguous mode selection for downstream agent behavior.
"""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class SubtaskClassificationPrompt:
    """Standardized prompt template for classifying user questions into task modes.

    This class provides a single LangChain `ChatPromptTemplate` (UNIFIED) that
    determines whether a user question should be answered with:
        - **ANALYSIS** (generate code for data processing, algorithms, or computations)
        - **VISUALIZATION** (generate plots, charts, or visual outputs)
        - **DIRECT_RESPONSE** (answer directly using existing summaries)

    Classification strictly follows rules that account for user intent,
    prior summaries, and pending context. The design ensures consistency
    in downstream agent behavior and prevents ambiguity.

    Attributes:
        UNIFIED:
            A classification prompt that:
                - Considers the user's current question.
                - Uses analysis and visualization summaries as context.
                - Accounts for pending context (recent model suggestions awaiting confirmation).
            The output is strictly one of: `ANALYSIS`, `VISUALIZATION`, or `DIRECT_RESPONSE`.
    """

    UNIFIED: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
You are a classification assistant.

You have access to:
- **Analysis Summary**: summary of all prior analyses performed.
- **Visualization Summary**: summary of all prior visualizations generated.
- **Pending Context**: the most recent suggested immediate action awaiting confirmation.

Your task is to decide the **mode of response** for the user's question.

## MODES
- **ANALYSIS** → generate executable code for analysis only (no visualizations).
- **VISUALIZATION** → generate visualizations/plots only (no additional code).
- **DIRECT_RESPONSE** → if the provided summaries contain enough information to fully answer the user's question.

## STRICT RULES
1. Output must be exactly one word: `ANALYSIS`, `VISUALIZATION`, or `DIRECT_RESPONSE`.
2. If the user's request involves calculations, data processing, or algorithms → choose `ANALYSIS`.
3. If the user's request involves plots, charts, or other visuals → choose `VISUALIZATION`.
4. If the user's request can be fully answered using the analysis and visualization summaries → choose `DIRECT_RESPONSE`.
5. Never mix modes. Only select one mode per question.
6. **Pending Context Handling**:
   - If the CURRENT user question **explicitly or implicitly confirms, agrees with, or relates to a prior suggestion or Pending Context**, ALWAYS follow the Pending Context action type (`ANALYSIS` or `VISUALIZATION`).
   - In these cases, **never output `DIRECT_RESPONSE`**, even if summaries contain enough information.
   - If no Pending Context exists or the question does not relate to it, follow the normal rules (1–5).
"""
            ),
            HumanMessagePromptTemplate.from_template(
                """
User question: {question}

Analysis Summary: {analysis_summary}
Visualization Summary: {visualization_summary}
Pending Context: {pending_context}
"""
            ),
        ]
    )
