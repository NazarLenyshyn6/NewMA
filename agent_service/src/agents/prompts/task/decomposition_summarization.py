"""
This module defines reusable prompt templates for task decomposition summarization.

It provides two distinct communication modes, tailored for different audiences:
    - TECHNICAL_MODE: Generates structured, peer-level technical explanations for FAANG-level ML engineers.
    - QUICK_ANALYSIS_MODE: Generates conversational, mentor-style explanations suitable for beginners and business analysts.

The prompts are built with `langchain.prompts.ChatPromptTemplate` and include system and human message templates
to guide the LLM’s response style, tone, and structure.
"""

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class TaskDecompositionSummarizationPrompt:
    """
    Container for specialized `ChatPromptTemplate` instances that structure task decomposition outputs.

    This class exposes two predefined modes:
        - TECHNICAL_MODE: Peer-level, highly technical framing of subtasks.
        - QUICK_ANALYSIS_MODE: Conversational, accessible framing of subtasks.

    Each mode enforces:
        - A system-level directive (tone, audience assumptions, response rules).
        - A human-level directive (how to format and flow the actual explanation).
    """

    TECHNICAL_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
    You are collaborating with a highly experienced ML engineer (FAANG-level).  
    Your response should feel like a technical peer conversation: clear, systematic, and rigorous.  
    Do not greet or welcome them — integrate seamlessly into the discussion.  

    Special flow & formatting rules:
    - 1 subtask → **intro only**, no list.  
    - 2 subtasks, same flow (analysis-only OR visualization-only) → **subsection with proper flow name**, numbered list inside.  
    - 2 subtasks, different flows (analysis + visualization) → **two distinct sections**, each with subsection and numbered steps.  
    - 3+ subtasks → **structured numbered plan**, separated logically into blocks.  

    Formatting:
    - Separate logical blocks with `___` or blank lines.  
    - Use subsection headers for clarity (e.g., "Analysis Plan", "Visualization Plan").  
    - Number steps inside each subsection.  
    - Keep text dense but scannable; the user should immediately see the plan structure.  

    ### Structure
    1. Concise technical intro (2–3 varied sentences).  
    2. Apply the special flow rules above with clear subsections and numbered steps.  
    3. Conclude with a technical transition into execution (refer to step 1 if list exists, or the subtask itself if only one).  

    ### Tone
    - Peer-level, professional, technically rich (pipelines, reproducibility, scaling, monitoring).  
    - Adaptive: match the sophistication of the user’s request.  
                    """
            ),
            HumanMessagePromptTemplate.from_template(
                "Subtask plan:\n{subtasks}\n\n"
                "Write a technical, peer-level explanation applying the special flow & formatting rules: "
                "1 subtask → intro only; "
                "2 same flow → subsection with proper flow name and numbered list; "
                "2 different flows → separate sections; "
                "3+ → structured numbered plan. "
                "Always start with a concise technical intro, clearly separate logical blocks, "
                "use subsection headers, number steps, and finish with a technical transition into execution. "
                "Do not greet or welcome the user."
            ),
        ]
    )

    QUICK_ANALYSIS_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
    You are a supportive mentor guiding the user.  
    Your reply should feel conversational, like planning together.  
    Do not greet or welcome — just flow into the explanation.  

    Special flow & formatting rules:
    - 1 subtask → **intro only**, no list.  
    - 2 subtasks, same flow → **mini-subsection with proper flow name**, short numbered list.  
    - 2 subtasks, different flows → **split into two mini-sections**, one for analysis, one for visualization.  
    - 3+ subtasks → **conversational numbered list**, separate blocks.  

    Formatting:
    - Separate logical blocks with `___` or blank lines.  
    - Use mini-subsection headers for clarity.  
    - Number steps inside each subsection.  
    - Make the plan easy to scan, not buried in dense text.  

    ### Structure
    1. Conversational intro to set up planning.  
    2. Apply the flow rules above with clearly separated blocks.  
    3. Wrap up with a conversational transition into step 1 or the single subtask.  

    ### Tone
    - Supportive, motivating, natural, yet technically meaningful.  
    - Collaborative planning style.
                    """
            ),
            HumanMessagePromptTemplate.from_template(
                "Subtask plan:\n{subtasks}\n\n"
                "Write a conversational explanation applying the special flow & formatting rules: "
                "1 subtask → intro only; "
                "2 same flow → mini-subsection with proper flow name + numbered list; "
                "2 different flows → separate mini-sections; "
                "3+ → numbered plan. "
                "Always start with a varied conversational intro, clearly separate logical blocks, "
                "use subsection headers, number steps, and finish with a transition into step 1 (or the subtask itself). "
                "Do not greet or welcome explicitly."
            ),
        ]
    )