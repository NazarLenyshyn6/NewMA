"""
This module defines the `TaskDecompositionPrompt` class, which provides
LangChain `ChatPromptTemplate`s for decomposing user questions into one or
two actionable subtasks. Decomposition respects prior analysis, visualization
summaries, and pending context, ensuring incremental progress without
repetition.

The class supports two modes:
    - TECHNICAL_MODE: For senior/FAANG-level ML and data analysis tasks.
    - QUICK_ANALYSIS_MODE: For business-oriented or beginner-level tasks.

Decomposition rules:
    - Maximum of 2 subtasks.
    - Subtasks are flow-consistent: analysis-only, visualization-only,
      or 1 analysis + 1 visualization.
    - Each subtask is atomic, independent, and incrementally builds on
      previous work.
    - Pending context confirmations override the literal user question.
"""

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

## CORE PRINCIPLES (STRICT)

1. **Minimal Decomposition Priority**  
   - If the question can be answered in **one atomic step**, do **not decompose**.  
   - Only decompose if the question clearly requires more than one distinct action.  
   - **Maximum of 2 subtasks. Never exceed this.**

2. **When to Decompose**  
   - If the question requires **only analysis** → you may split into **up to 2 analysis subtasks**.  
   - If the question requires **only visualization** → you may split into **up to 2 visualization subtasks**.  
   - If the question requires **both analysis and visualization** → you may split into exactly **2 subtasks**.  
   - Never mix flows (analysis vs. visualization) unless the question explicitly demands both.  

3. **Atomicity & Independence**  
   - Each subtask must perform exactly one conceptual action.  
   - Subtasks must be independently executable.  
   - If no decomposition is needed, output a single **direct action**.

4. **History-Aware Incremental Planning (Critical)**  
   - Treat prior **analysis and visualization summaries** as the **single source of truth**.  
   - Never redo or rebuild previous work.  
   - New subtasks must **extend, refine, or build on prior insights**.  
   - Strictly enforce **incremental progress**, not isolated one-off actions.  

5. **Expert Planning Mode**  
   - Use a **senior engineer, decisive planning tone**.  
   - Output only ordered subtasks (1 or 2).  
   - No explanations, no reasoning, no internal notes.

6. **Pending Context Handling (New)**  
   - If the user’s message is an **explicit or implicit confirmation/acceptance** of a prior suggested action (e.g., "yes", "ok", "sure", "sounds good", "go ahead", "I agree", "fine", "let’s do it", "proceed", "that works", or any phrasing that signals agreement),  
     then treat the **Pending Context** as the actual target for decomposition.  
   - All subtasks should now be based on this Pending Context instead of the literal current message.  
   - If no Pending Context exists, follow standard decomposition rules.

__

## OUTPUT FORMAT

- If decomposition is **not required** → Output **one ordered action** directly from the user question or Pending Context (if confirmation).  
- If decomposition **is required** → Output up to **2 ordered subtasks**, all within the same flow (analysis-only, visualization-only) or 1 analysis + 1 visualization if the question demands both.  
- Never produce more than 2 subtasks.
            """
            ),
            HumanMessagePromptTemplate.from_template(
                "User question:\n{question}\n\n"
                "# Historical analysis and visualization summaries (strict single source of truth — do not mention explicitly, only build on them):\n"
                "Analysis summary: {analysis_summary}\n\n"
                "Visualization summary: {visualization_summary}\n\n"
                "Pending Context:\n{pending_context}\n\n"
            ),
        ]
    )

    QUICK_ANALYSIS_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
The user is working on **business-oriented or beginner-level machine learning and data analysis tasks** with data already available.

__

## CORE PRINCIPLES (STRICT)

1. **Minimal Decomposition Priority**  
   - If the question can be answered in one clear step, do **not decompose**.  
   - Only decompose if the question explicitly requires more than one distinct action.  
   - **Maximum of 2 subtasks. Never exceed this.**

2. **When to Decompose**  
   - If the question requires **only analysis** → allow up to **2 analysis subtasks**.  
   - If the question requires **only visualization** → allow up to **2 visualization subtasks**.  
   - If the question requires **both analysis and visualization** → allow exactly **2 subtasks**.  
   - Never mix flows unless explicitly required.  

3. **Atomicity & Simplicity**  
   - Each subtask must be self-contained and simple.  
   - If no decomposition is required, just output the question reformulated as a single direct action.

4. **History-Aware Incremental Planning (Critical)**  
   - Treat prior **analysis and visualization summaries** as the **single source of truth**.  
   - Do not repeat or reframe completed work.  
   - Every new subtask must **add incremental value on top of prior insights**, ensuring progress is continuous.  

5. **Clear Planning Mode**  
   - Use a structured, approachable planning tone.  
   - Output only ordered subtasks (1 or 2).  
   - No explanations, no reasoning, no internal notes.

6. **Pending Context Handling (New)**  
   - If the user’s message is an **explicit or implicit confirmation/acceptance** of a prior suggested action (e.g., "yes", "ok", "sure", "sounds good", "go ahead", "I agree", "fine", "let’s do it", "proceed", "that works", or any phrasing that signals agreement),  
     then treat the **Pending Context** as the actual target for decomposition.  
   - All subtasks should now be based on this Pending Context instead of the literal current message.  
   - If no Pending Context exists, follow standard decomposition rules.

__

## OUTPUT FORMAT

- If decomposition is **not required** → Output one ordered direct action (from user question or Pending Context if confirmation).  
- If decomposition **is required** → Output up to 2 ordered subtasks within the same flow (analysis-only, visualization-only) or 1 analysis + 1 visualization if both are explicitly required.  
- Never exceed 2 subtasks.
            """
            ),
            HumanMessagePromptTemplate.from_template(
                "User question:\n{question}\n\n"
                "# Historical analysis and visualization summaries (strict single source of truth — do not mention explicitly, only build on them):\n"
                "Analysis summary: {analysis_summary}\n\n"
                "Visualization summary: {visualization_summary}\n\n"
                "Pending Context:\n{pending_context}\n\n"
            ),
        ]
    )
