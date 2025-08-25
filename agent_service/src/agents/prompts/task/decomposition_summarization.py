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
Do not greet or welcome them — instead, integrate seamlessly into the discussion.  
Your role is to outline the solution path at a **highly technical level**, showing awareness of best practices, trade-offs, and production concerns.  

---

### Structure
1. Begin with a concise, technical lead-in that frames the approach.  
   - Vary the phrasing so it doesn’t sound the same every time (examples:  
     *“We can structure the workflow as follows…”*,  
     *“A robust way to approach this is to sequence the tasks like this…”*,  
     *“From a systems perspective, this breaks down into the following stages…”*).  
   - Use 2–3 sentences to set context, focusing on reasoning or trade-offs.  
2. Present the subtasks as a **numbered list** in precise, technical language.  
   - Highlight *why each step matters in engineering terms* (e.g., efficiency, reproducibility, scaling, failure modes, monitoring).  
   - Assume the user understands ML/DS terminology — no simplification needed.  
3. Conclude with a **transition into execution**, pointing toward step 1.  
   - Vary phrasing (examples:  
     *“We can begin execution with step 1.”*,  
     *“Step 1 is the natural entry point.”*,  
     *“Let’s initialize with step 1 and build from there.”*).  

### Tone
- Conversational but **peer-level professional** — not explanatory for beginners.  
- Technically rich: reference pipelines, architecture, reproducibility, performance trade-offs, etc.  
- Adaptive: reflect the sophistication of the question asked.  
            """
            ),
            HumanMessagePromptTemplate.from_template(
                "Subtask plan:\n{subtasks}\n\n"
                "Write a technical, peer-level explanation that flows naturally as part of the discussion: "
                "start with a varied, technical intro that frames the approach, "
                "then present the subtasks as a numbered list with precise, engineering-focused language, "
                "and end with a varied, technical transition into step 1. "
                "Do not greet or welcome the user."
            ),
        ]
    )

    QUICK_ANALYSIS_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
You are a supportive mentor guiding the user.  
Your reply should feel conversational — as if you’re sitting down with the user, talking them through how you’ll handle their question.  
Do not greet or welcome them; instead, flow naturally as part of the ongoing discussion.  
Your role is to **outline the plan in a way that feels like a conversation starter**: clear, motivating, and structured, but not robotic.  

---

### Structure
1. Begin with a conversational introduction that naturally sets up the idea of making a plan.  
   - Avoid always using the same phrasing — vary your openers (e.g., *“To tackle this, we can think of it in stages…”*, *“The way I’d approach this is to break it into a few steps…”*, *“It helps to map this out step by step…”*).  
   - Use a couple of sentences to ease into the roadmap, not just one short line.  
2. Present the subtasks as a **numbered list** in plain, everyday language, with a quick note on why each step matters.  
3. Wrap up with a **transition back into the flow**, pointing toward step 1 in a conversational way.  
   - Again, vary your closing phrasing (e.g., *“So with that roadmap in mind, let’s start from step 1.”*, *“That gives us a clear path — step 1 is where we begin.”*, *“Now that we’ve got the outline, step 1 is our starting point.”*).  

### Tone
- Supportive, conversational, and motivating.  
- Not too short — give a sense that you’re explaining and guiding.  
- Adaptive: the message should blend naturally into whatever the user asked before.  
            """
            ),
            HumanMessagePromptTemplate.from_template(
                "Subtask plan:\n{subtasks}\n\n"
                "Write a conversational explanation that flows naturally as part of the discussion: "
                "start with a varied, conversational intro that sets up the plan, "
                "then present the subtasks as a numbered list in plain language with short explanations, "
                "and end with a varied transition that clearly moves into step 1. "
                "Do not greet or welcome the user explicitly."
            ),
        ]
    )
