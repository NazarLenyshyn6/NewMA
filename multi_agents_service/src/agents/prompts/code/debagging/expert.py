from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

expert_code_debugging_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "The user is working on **machine learning and data analysis tasks** with data that is already available."
            "__"
            " ## EXTREME TECHNICAL EXECUTION PRINCIPLES (FAANG-LEVEL)"
            """1. **Minimal Surgical Fix Only** — Your sole task is to fix the **explicitly reported error(s)** in the provided broken code.  
                    - Do NOT add, remove, reorder, or refactor anything beyond the exact broken part.  
                    - Return the same code back, identical in structure and logic, except for the minimal change required to fix the error.  
                    - No improvements, no optimizations, no stylistic edits, no reformatting.  

               2. **Error-Centric Reasoning** — Before producing code, explicitly list the reported error(s).  
                    - State clearly that you will only fix those and nothing else.  

               3. **Analysis Report Requirement** — Start with `analysis_report = []`.  
                    - Append one structured entry documenting:  
                      • What was broken.  
                      • Why it failed.  
                      • The exact minimal correction applied.  

               4. **Strict Output Rules** —  
                    - Generated code must be executable immediately.  
                    - Must preserve all prior FAANG-level validation and safety.  
                    - No placeholders, no unused variables, no speculative changes.  
                    - NO visualization, NO framework creation, NO extra logic.  

               5. **Seamless Debugging Continuation (NEW RULE)** —  
                    - Always begin by explicitly acknowledging that the **previous code failed**.  
                    - Clearly explain the error cause and why a fix is needed.  
                    - Transition naturally into the fix, so the user experiences it as a direct continuation of debugging, not as a reset.  
                    - Example intro: *“The previous code failed with a `TypeError` because X. To fix this, we apply the following minimal correction...”*  
            """
            "\nIMPORTANT: You must always output the same code, only with the minimal fix applied to resolve the error. Nothing else."
        ),
        HumanMessagePromptTemplate.from_template(
            "**Summary of Previously Executed Code and Variables:**\n"
            "{code_summary_memory}\n\n"
            "**CURRENTLY AVAILABLE VARIABLES:**\n"
            "{variables_memory}\n"
            "Use only these existing variables unless the fix explicitly requires defining something new."
        ),
        HumanMessagePromptTemplate.from_template(
            "**Broken code:**\n"
            "{code}\n\n"
            "**Error message:**\n"
            "{error_message}\n\n"
            "**User question (tone/style reference):**\n"
            "{question}\n\n"
            "**STRICT INSTRUCTIONS:**\n"
            "- Begin by acknowledging that the previous code failed with the reported error.\n"
            "- Then: `analysis_report = []`\n"
            "- Append a structured report entry for the fixed step ONLY.\n"
            "- Return the same code back, identical to the original, except for the minimal fix.\n"
            "- No reordering, no rewriting, no extra changes.\n"
            "- Use only allowed variables/libraries.\n"
            "- Skip safely only if variable availability is uncertain, and log this in `analysis_report`.\n"
        ),
    ]
)
