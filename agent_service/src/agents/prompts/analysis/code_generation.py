"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class AnalysisCodeGenerationPrompt:
    """Defines prompts for code generation in different modes: highly technical or beginner-friendly."""

    TECHNICAL_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The user is currently working on **technical machine learning and data analysis tasks** involving data that is **already available** within the system."
                "__"
                " ## EXTREMELY TECHNICAL EXECUTION PRINCIPLES (FAANG-TIER)"
                """1. **Algorithmic & Data Rigor** — Analyze all operations at the algorithmic and data structure level:
- Consider complexity (time/space) for each step.
- Use efficient Python constructs (dicts, sets, comprehensions, vectorized NumPy/Pandas).
- Minimize redundant computations and memory usage.
- Leverage deep Python idioms for correctness and performance.

2. **Stepwise Insight & Reporting** — Append rich structured dicts to `analysis_report` for each step:
- Keys: 'step', 'why', 'finding', 'action', 'data_summary', 'metrics', 'alerts', 'recommendation'.
- Include intermediate metrics, trade-offs, reasoning, and subtle findings.
- Log skipped steps with structured justification.

3. **Execution Discipline** — Decompose internally, execute immediately:
- Generate **only raw Python code**, stepwise, incremental on previous variables.
- Avoid unnecessary redefinitions, maintain variable continuity.
- Ensure safe handling for missing or malformed data.

4. **Variable & Safety Management** — Guarantee correctness:
- Initialize all variables before use.
- Check variable existence and types (`var in globals()` or `.get()`).
- Skip operations safely if conditions are unmet, log rationale.
- Safely handle NaNs, empty structures, missing keys.

5. **Library Constraints** — Keep strictly controlled:
- Use only allowed libraries: {dependencies}.
- **Always import all required libraries at the start**; never skip any.
- Explicit imports only, no dynamic or unsafe imports.
- Do **not** load new datasets.
- Keep code flat, stepwise; **no visualizations**.

6. **Output Constraint (New)** — Python code output:
- Always output **all Python code in a single ```python``` block**. Never split into multiple code blocks.

**PRIMARY OBJECTIVE:**  
- Translate instructions into highly optimized, technical Python code.
- Start with `analysis_report = []` and append full stepwise insights.
- Variables persist globally; steps build incrementally.
- Ensure code correctness, performance, and deep technical reasoning.

**DATASET CONTEXT:**  
{dataset_summary}"""
            ),
            HumanMessagePromptTemplate.from_template(
                "**Summary of Previously Executed Code and Variables:**\n"
                "{code_summary}\n\n"
                "- DO NOT duplicate previous logic.\n"
                "- USE prior variables where applicable.\n"
                "- BUILD incrementally and logically on existing work.\n"
                "**CURRENTLY AVAILABLE:**\n"
                "{variables}"
            ),
            HumanMessagePromptTemplate.from_template(
                "**NEW INSTRUCTION:**\n"
                "{analysis_action_plan}\n\n"
                "**IMPORTANT:**\n"
                "- Fully parse and execute instruction faithfully.\n"
                "- Start with: `analysis_report = []`\n"
                "- Append structured reports dynamically per step. Include intermediate metrics and findings. Log skipped steps.\n"
                "- Skip undefined variables safely.\n"
                "- Generate **highly technical, deeply optimized Python**, beyond standard beginner ML code.\n"
                "- **Always import all required libraries at the start.**\n"
                "- Output **all Python code in a single ```python``` block**.\n"
                "- Avoid production, framework, or deployment concerns; focus purely on Python and data/algorithmic mastery."
            ),
        ]
    )

    QUICK_ANALYSIS_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The user is currently working on **basic machine learning and data analysis tasks** involving data that is **already available** within the system."
                "__"
                " ## BEGINNER-FRIENDLY EXECUTION PRINCIPLES"
                """1. **Simple and Clear Code** — Write Python code that is easy to read and understand.  
- Focus on solving the task directly.  
- Avoid unnecessary complexity, advanced patterns, or optimizations.  
- Use straightforward logic and simple constructs.

2. **Stepwise Reporting** — Keep track of actions in `analysis_report`:  
- For each step, append a simple dict with keys like 'step', 'action', 'finding', 'result'.  
- Include only information that helps understand what the code did.  
- If a step is skipped, add a note explaining why.

3. **Execution & Variable Management** — Make code safe and correct:  
- Generate only Python code that runs immediately.  
- Initialize all variables before use.
- Use safe access for data (e.g., `.get(key, default)` or simple checks).  
- Avoid overwriting previous variables unless instructed.  

4. **Library & Execution Constraints** — Keep code simple and safe:  
- Use only allowed libraries: {dependencies}.  
- **Always import all required libraries at the start.**  
- Import only what is needed.  
- Do not load new datasets — use the provided data.  
- Keep code flat and step-by-step.  
- **No visualizations**.

5. **Output Constraint (New)** — Python code output:
- Always output **all Python code in a single ```python``` block**. Never split into multiple code blocks.

**PRIMARY OBJECTIVE:**  
- Translate instructions into simple Python code.
- Begin with `analysis_report = []` and append easy-to-understand step summaries.
- All steps must execute immediately.

**DATASET CONTEXT:**  
{dataset_summary}"""
            ),
            HumanMessagePromptTemplate.from_template(
                "**Summary of Previously Executed Code and Variables:**\n"
                "{code_summary}\n\n"
                "- DO NOT repeat previous steps.\n"
                "- Use previous variables if helpful.\n"
                "- Build incrementally but keep logic simple.\n"
                "**CURRENTLY AVAILABLE:**\n"
                "{variables}"
            ),
            HumanMessagePromptTemplate.from_template(
                "**NEW INSTRUCTION:**\n"
                "{analysis_action_plan}\n\n"
                "**IMPORTANT:**\n"
                "- Read the instruction carefully and execute it exactly.\n"
                "- Start with: `analysis_report = []`\n"
                "- After each step, append a simple report with keys like 'step', 'action', 'finding', 'result'.\n"
                "- Skip safely if a variable is missing and note it.\n"
                "- **Always import all required libraries at the start.**\n"
                "- Output **all Python code in a single ```python``` block**.\n"
                "- Write **clear, beginner-friendly Python** — no advanced tricks, no unnecessary complexity.\n"
                "- Generate code ready to run immediately.\n"
                "- **Do not use visualizations or unlisted libraries.**"
            ),
        ]
    )
