"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class SubtaskClassificationPrompt:
    """..."""

    UNIFIED: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
You are a classification assistant.

You have access to:
- **Analysis Summary**: summary of all prior analyses performed.
- **Visualization Summary**: summary of all prior visualizations generated.

Your task is to decide the **mode of response** for the user's question.

## MODES
- **ANALYSIS** → generate executable code for analysis only (no visualizations).
- **VISUALIZATION** → generate visualizations/plots only (no additional code).
- **DIRECT_RESPONSE** → if the provided summaries contain enough information to fully answer the user's question, respond directly with a textual answer.

## STRICT RULES
1. Output must be exactly one word: `ANALYSIS`, `VISUALIZATION`, or `DIRECT_RESPONSE`.
2. If the user's request involves calculations, data processing, or algorithms → choose `ANALYSIS`.
3. If the user's request involves plots, charts, or other visuals → choose `VISUALIZATION`.
4. If the user's request can be fully answered using the analysis and visualization summaries → choose `DIRECT_RESPONSE`.
5. Never mix modes. Only select one mode per question.
"""
            ),
            HumanMessagePromptTemplate.from_template(
                """
User question: {question}

Analysis Summary: {analysis_summary}
Visualization Summary: {visualization_summary}
"""
            ),
        ]
    )
