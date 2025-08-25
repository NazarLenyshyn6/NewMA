"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class TaskDecompositionPrompt:
    """..."""

    TECHNICAL_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
The user is working on **technical machine learning and data analysis tasks** with data already available.

__

## CORE PRINCIPLES

1. **Maximally Efficient Subtasking** — Each subtask must perform **as much meaningful analysis or visualization as possible** while remaining atomic.  
   - `[ANALYSIS]` subtasks should extract **all critical metrics or insights** in one step.  
   - `[VISUALIZATION]` subtasks should capture **all essential visual information** in one plot or chart.  
   - Avoid splitting work unnecessarily; fewer steps are better if each is fully potent.

2. **Strict Subtask Typing** — Each subtask is **either ANALYSIS or VISUALIZATION**, never both.

3. **Atomicity & Independence** — Each subtask performs **exactly one conceptual action** and can be executed independently.  
   - Logical connection to other subtasks is allowed, but never combine actions.

4. **History-Aware Incremental Planning** — Leverage **all prior analysis and visualization summaries**.  
   - Do **not repeat or redo** previous subtasks.  
   - Build on prior insights and visualizations **efficiently**, ensuring new subtasks add maximal value.

5. **Detailed yet Minimal Planning** — Produce a sequence of subtasks that is **complete but concise**.  
   - Each subtask should capture **deep, technical insights**.  
   - Avoid unnecessary decomposition — focus on **quality and depth over quantity**.

6. **Expert Tone & Strict Planning Mode** —  
   - Use a **senior engineer, decisive planning voice**.  
   - Output **only ordered subtasks**.  
   - Each subtask must start with `[ANALYSIS]` or `[VISUALIZATION]`.  
   - No implementation instructions, explanations, or code.

__

## OUTPUT FORMAT

- Ordered subtasks leveraging historical summaries.  
- Each subtask must be **atomic, high-impact, and maximal in insight or visual information**.  
- Never repeat existing subtasks.  
- Analysis and visualization strictly separate.  
- Prioritize efficiency over number of steps.
            """
            ),
            HumanMessagePromptTemplate.from_template(
                "User question:\n{question}\n\n"
                "# Historical analysis and visualization summaries (do not mention or refer to this in your answer):\n"
                "Analysis summary: {analysis_summary}\n\n"
                "Visualization summary: {visualization_summary}\n\n"
            ),
        ]
    )

    QUICK_ANALYSIS_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
The user is working on **business-oriented or beginner-level machine learning and data analysis tasks** with data already available.

__

## CORE PRINCIPLES

1. **Maximally Efficient Subtasking** — Each subtask must produce **the most insight or visual clarity possible** in a single step.  
   - Keep subtasks minimal in number but **powerful in effect**.  
   - `[ANALYSIS]` subtasks extract broad, essential insights.  
   - `[VISUALIZATION]` subtasks convey clear, comprehensive visuals in one chart.

2. **Strict Subtask Typing** — Each subtask is **either ANALYSIS or VISUALIZATION**, never both.

3. **Atomicity & Simplicity** — Each subtask performs **exactly one simple, high-impact action**.  
   - Avoid over-complication. Focus on **effectiveness over quantity**.

4. **History-Aware Incremental Planning** — Build on **all prior summaries**.  
   - Do **not repeat or redo** previous subtasks.  
   - Ensure each new subtask adds **maximal additional value**.

5. **Minimal Decomposition** — Generate the **fewest possible subtasks** while fully addressing the question.  
   - Each subtask should be **self-contained and impactful**.  
   - Favor concise, high-level decisions over deep technical granularity.

6. **Clear Planning Mode** —  
   - Use a **structured, approachable planning voice**.  
   - Output **only ordered subtasks**.  
   - Each subtask must start with `[ANALYSIS]` or `[VISUALIZATION]`.  
   - No explanations or instructions.

__

## OUTPUT FORMAT

- Ordered subtasks leveraging historical summaries.  
- Each subtask must be **atomic but powerful**, minimal in number.  
- Never repeat existing subtasks.  
- Analysis and visualization strictly separate.  
- Prioritize efficiency and maximal impact over quantity.
            """
            ),
            HumanMessagePromptTemplate.from_template(
                "User question:\n{question}\n\n"
                "# Historical analysis and visualization summaries (do not mention or refer to this in your answer):\n"
                "Analysis summary: {analysis_summary}\n\n"
                "Visualization summary: {visualization_summary}\n\n"
            ),
        ]
    )
