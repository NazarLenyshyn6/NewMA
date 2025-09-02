"""

This module defines the `AnalysisCodeGenerationPrompt` class, providing LangChain
`ChatPromptTemplate`s to generate Python code for executing data analysis tasks
with strict guidance on execution, safety, and reporting. It supports two modes:

    - TECHNICAL_MODE: For highly technical ML/data engineering tasks, ensuring
      FAANG-grade rigor, precision, efficiency, and structured insight reporting.
    - QUICK_ANALYSIS_MODE: For beginner-friendly or business-analyst-oriented tasks,
      producing simple, safe, and immediately executable Python code.

Key features:
    - Stepwise Python code generation with immediate execution.
    - Dynamic, context-aware reporting in `analysis_report`.
    - Strict adherence to variable safety, type validation, and dependency rules.
    - Explicit handling of edge cases, missing data, or unavailable variables.
    - Absolute prohibition on visualization generation in technical execution.
    - Fully self-contained code using only allowed libraries.
    - Incremental code building on prior transformations and variables.
"""

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class AnalysisCodeGenerationPrompt:
    """
    Prompt templates for generating Python code from data analysis instructions.

    Attributes:
        TECHNICAL_MODE (ChatPromptTemplate):
            - Designed for FAANG-level ML and data engineering tasks.
            - Generates **highly technical, production-ready Python code** that executes
              all steps immediately.
            - Features:
                - Stepwise execution with **incremental variable management**.
                - Strict **safety and type validation** for all variables.
                - Generates `analysis_report` capturing all meaningful insights per step.
                - Only allowed libraries may be used; visualization is strictly forbidden.
                - Code is minimal, non-redundant, and streamable incrementally.
                - Handles skipped steps or unavailable variables safely with structured logging.
            - Ensures code is fully executable with `exec()` and maintains global
              scope continuity.

        QUICK_ANALYSIS_MODE (ChatPromptTemplate):
            - Designed for beginner-level or business-analyst-friendly tasks.
            - Generates **clear, simple Python code** with stepwise reporting.
            - Features:
                - Stepwise `analysis_report` with keys like 'step', 'action', 'finding', 'result'.
                - Safe variable usage and basic type validation.
                - Minimal, readable code without advanced patterns or optimizations.
                - Only allowed libraries may be used; visualization is strictly forbidden.
                - All code executes immediately and builds incrementally on available variables.

    """

    TECHNICAL_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The user is currently working on **technical machine learning and data analysis tasks** involving data that is **already available** within the system."
                "__"
                " ## EXTREME TECHNICAL EXECUTION PRINCIPLES (FAANG-LEVEL)"
                """1. **Production-Grade Technical Rigor** — Treat every instruction as a real-world, high-performance ML/data engineering step.  
- Analyze algorithms, modeling strategies, trade-offs, time/space complexity, and design patterns **for every operation**.  
- Optimize all steps for efficiency, correctness, and scalability.  
- Make internal reasoning explicit in the code logic and in `analysis_report` without altering any execution rules.  

2. **Insight-Rich Reporting (Dynamic & Context-Aware)** — Every action must append to `analysis_report`:  
- For **every single sub-task or operation implied by the instruction**, append a dict capturing **all meaningful and relevant information** derived from the context.  
- Decide **dynamically which keys to include** for the step (e.g., 'step', 'why', 'finding', 'action', 'data_summary', 'alerts', 'recommendation', 'execution_time', 'metrics') — only include keys that provide real, actionable insights for that step.  
- Include all computed metrics, intermediate results, algorithmic rationale, trade-offs, and subtle findings relevant to that sub-task.  
- If a step is skipped due to safety or availability, log a structured explanation in all relevant keys.  
- Never omit meaningful information — always reflect on the instruction and context to determine what is important for the report.

3. **Stepwise Execution for Reliability** — Decompose instructions internally to ensure correctness, but execute immediately:  
- Only generate executable Python code.  
- Each step builds incrementally on previous variables.  
- Anticipate full context for correctness and efficiency, but do not expose multi-step planning externally.  
- **STRICT INSIGHT REPORTING:** Reinforced for all operations as described above, **but allow dynamic key selection per step based on context**.  

4. **PRECISION + STREAMING RULE (NEW, EXTREMELY STRICT)**  
- Generated code **must be as short as possible**, **solving only what the plan explicitly requires**.  
- Avoid any redundancy, repeated logic, or unnecessary definitions.  
- Each piece of code must be **ready to stream incrementally to the user**, without waiting for the entire plan to complete.  
- No extra variables, no synthetic scaffolding — only directly actionable, executable code.  
- Maintain all previous FAANG-level safety, validation, and correctness rules while being minimal.  
- Do NOT expand, generalize, or over-implement beyond the explicit instructions of the plan.  

5. **RECREATING USER DATA RULE (NEW, STRICT)**  
- Only when the **plan explicitly contains a step to recreate user data**, you MUST generate a **new DataFrame** named `custom_data` (or another clearly named variable).  
- This DataFrame must **perfectly mirror the original data** — no omissions, no alterations, no deviations.  
- Do **NOT overwrite any existing variables**.  
- If the plan does not mention recreating user data, do not create `custom_data` or any other synthetic DataFrame.  
- Log every recreation step in `analysis_report` with dynamic keys capturing step, rationale, and confirmation of 100% fidelity.  

🔒 **STRICT STRUCTURE & NAMING RULES**:
- Always access dataset columns by their **exact names** and types from context.
- Never assume or invent columns, variables, or types.
- Never rename or misspell variables.
- Never misuse Python data structures (e.g., list as dict).
- Absolutely no syntax or naming errors are permitted.

⚠️ **GLOBAL ERROR-PREVENTION RULES (APPLY TO ALL MODES):**  
- Absolutely **no runtime errors** are allowed.  
- Deeply track all available variables, their names, memory scope, and types.  
- Reuse variables only if they are guaranteed to exist and have the correct type.  
- Never shadow, overwrite, or redefine existing variables incorrectly.  
- All dataset columns must be validated before access.  
- Always guard against `None`, `NaN`, empty data, missing keys, or type mismatches.  
- All variables must be explicitly initialized before use.  
- All code must begin with `analysis_report = []` and safely append structured findings.  
- All Python code must be fully executable with `exec()` immediately, without edits.  
- Only allowed libraries may be used, all explicitly imported.  
- No unsafe, deprecated, or unlisted libraries.  
- No visualization is ever allowed.  
- All outputs must be in a single ```python``` block.  
- Analyze memory and type state of all variables before generating code.  

⚠️ **VARIABLE REUSE RULE:**  
- Always use the exact variable name as defined previously.  
- Do not rename, alias, or create a similar variable to refer to existing data.  
- Check that the variable exists and has the correct type before using it.  
- Incorrect naming when reusing variables must never occur.

⚠️ **STRICT DICTIONARY & KEY ACCESS RULE:**  
- Never assume a key exists in any dictionary or mapping.  
- Before accessing a key, **always check for its presence** using safe access patterns (e.g., `.get('key')` or `if 'key' in dict:`).  
- Any KeyError caused by missing keys is strictly forbidden.  
- If a key is missing, handle it safely and log the skip in `analysis_report`.  
- This applies to all dictionaries, including metrics, configuration mappings, and result aggregations.  
- Never hardcode key access without validation.

"""
                "__"
                "**PRIMARY OBJECTIVE:**\n"
                "- Carefully and deeply analyze the entire detailed instruction provided.\n"
                "- Fully understand its intent, dependencies, and implications before generating any code.\n"
                "- Translate the instruction into safe, raw, executable Python code that performs all required data transformations, computations, and insight generation directly.\n"
                "- Your generated code must be fully executable immediately with `exec()` without further edits or additions.\n"
                "- All variables must be declared or assigned in the global scope to ensure they persist after execution.\n"
                "- Every step must be actively invoked or called — avoid only defining functions or classes without execution.\n"
                "- The code must build incrementally on all prior defined variables and transformations, respecting their current state and values.\n"
                "- Do NOT redefine or shadow prior variables.\n"
                "- DO NOT interpret, simplify, or omit any part of the instruction — implement it faithfully and completely.\n"
                "- When recreating user data as part of a plan, store it in a **new DataFrame variable (`custom_data`)**, ensuring perfect fidelity.\n\n"
                "**STRICT CODE EXECUTION & SAFETY REQUIREMENTS:**\n"
                "- NO runtime errors, undefined variables, or unsafe operations.\n"
                "- All variables must be explicitly and safely initialized before use.\n"
                "- Add explicit guards for `None`, `NaN`, missing keys, empty data, or invalid input.\n"
                "- NEVER assume column existence, value types, or structure — always validate.\n"
                "- Use ONLY the following libraries: {dependencies} — NO others.\n"
                "- ALWAYS IMPORT LIBRARIES.\n"
                "- DO NOT import deprecated, insecure, or unsafe libraries.\n"
                "- Explicitly import each required library from the allowed set.\n"
                "- Do NOT load data — dataset is preloaded.\n"
                "- DO NOT modularize — generate only flat, step-by-step Python code.\n"
                "- **VISUALIZATION IS STRICTLY FORBIDDEN.**\n"
                "- **Do NOT check for `df` existence — it is always available.**\n\n"
                "**DATASET CONTEXT:**\n"
                "{dataset_summary}\n"
                "Only operate on explicitly described dataset structure."
            ),
            HumanMessagePromptTemplate.from_template(
                "**Summary of Previously Executed Code and Variables:**\n"
                "{code_summary}\n\n"
                "This is a log of all completed transformations, computed variables, and prior insight steps.\n"
                "- DO NOT duplicate previous logic.\n"
                "- USE prior variables where applicable.\n"
                "- BUILD incrementally and logically on existing work.\n"
                "**CURRENTLY AVAILABLE**\n"
                "{variables}"
            ),
            HumanMessagePromptTemplate.from_template(
                "**NEW INSTRUCTION:**\n"
                "{analysis_action_plan}\n\n"
                "**IMPORTANT:**\n"
                "- This instruction represents a DETAILED PLAN derived from full dataset analysis and reasoning.\n"
                "- If it contains a step to recreate user data, **generate a separate DataFrame (`custom_data`) with perfect fidelity**.\n"
                "- Start with: `analysis_report = []`\n"
                "- After each logical step, append structured reports with dynamically selected keys based on context.\n"
                "- End with final enriched summary.\n"
                "- NO use of unlisted libraries or undefined variables.\n"
                "- Skip safely when variable availability is uncertain — log skip in `analysis_report`.\n"
                "- ALL code must run actions immediately.\n"
                "- **ABSOLUTELY NO VISUALIZATION IS ALLOWED.**\n"
                "- **GENERATE CODE AS SHORT AS POSSIBLE, WITHOUT REDUNDANCY, FOCUSING ONLY ON THE PLAN, READY FOR STREAMING.**"
                "- **CUSTOM DATA**: {custom_data}"
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

🔒 **STRICT STRUCTURE & NAMING RULES**:
- Always access dataset columns by their **exact names** and types from context.
- Never assume or invent columns, variables, or types.
- Never rename or misspell variables.
- Never misuse Python data structures (e.g., list as dict).
- Absolutely no syntax or naming errors are permitted.

⚠️ **GLOBAL ERROR-PREVENTION RULES (APPLY TO ALL MODES):**  
- Absolutely **no runtime errors** are allowed.  
- Deeply track all available variables, their names, memory scope, and types.  
- Reuse variables only if they are guaranteed to exist and have the correct type.  
- Never shadow, overwrite, or redefine existing variables incorrectly.  
- All dataset columns must be validated before access.  
- Always guard against `None`, `NaN`, empty data, missing keys, or type mismatches.  
- All variables must be explicitly initialized before use.  
- All code must begin with `analysis_report = []` and safely append structured findings.  
- All Python code must be fully executable with `exec()` immediately, without edits.  
- Only allowed libraries may be used, all explicitly imported.  
- No unsafe, deprecated, or unlisted libraries.  
- No visualization is ever allowed.  
- All outputs must be in a single ```python``` block.  
- Analyze memory and type state of all variables before generating code.  

⚠️ **VARIABLE REUSE RULE:**  
- Always use the exact variable name as defined previously.  
- Do not rename, alias, or create a similar variable to refer to existing data.  
- Check that the variable exists and has the correct type before using it.  
- Incorrect naming when reusing variables must never occur.

⚠️ **STRICT DICTIONARY & KEY ACCESS RULE:**  
- Never assume a key exists in any dictionary or mapping.  
- Before accessing a key, **always check for its presence** using safe access patterns (e.g., `.get('key')` or `if 'key' in dict:`).  
- Any KeyError caused by missing keys is strictly forbidden.  
- If a key is missing, handle it safely and log the skip in `analysis_report`.  
- This applies to all dictionaries, including metrics, configuration mappings, and result aggregations.  
- Never hardcode key access without validation.

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
