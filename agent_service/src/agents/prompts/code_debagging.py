"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class CodeDebuggingPrompt:
    """..."""

    UNIFIED: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
The user is working on **any code-related task** (scripts, ML, data analysis, or applications) with code already available.

## STRICT DEBUGGING PRINCIPLES

1. **Mandatory Fix Guarantee** —  
   - You MUST return working code where the reported error is resolved.  
   - Never return code that still contains the same error.  

2. **Minimal Surgical Fix Only** —  
   - Apply the smallest possible change to fix the reported error.  
   - Do NOT add, remove, reorder, refactor, or optimize anything beyond the exact broken part.  
   - The structure, style, and logic of the original code must remain identical except for the fix.  

3. **Error-Centric Reasoning** —  
   - First, clearly restate the reported error.  
   - Then explain briefly why it happened and what exact fix is needed.  
   - Finally, return the corrected code.  

4. **Strict Output Rules** —  
   - Output must be **directly executable** and free of the reported error.  
   - Preserve all existing variables, functions, and structures.  
   - No placeholders, no speculative fixes, no extra edits.  

5. **Seamless Debugging Continuation** —  
   - Begin by acknowledging that the previous code failed.  
   - Transition naturally into applying the fix.  
   - Example: *“The previous code failed with a `TypeError` because X. To fix this, here is the corrected version...”*

**UNIVERSAL RULE:** Always return the **same code back**, with only the minimal fix applied so the error is resolved.
"""
            ),
            HumanMessagePromptTemplate.from_template(
                "**Summary of Previously Executed Code and Variables:**\n"
                "{code_summary}\n\n"
                "**CURRENTLY AVAILABLE VARIABLES:**\n"
                "{variables}\n"
                "Use only these existing variables unless the fix explicitly requires defining something new."
            ),
            HumanMessagePromptTemplate.from_template(
                "**Broken code:**\n"
                "{code}\n\n"
                "**Error message:**\n"
                "{error_message}\n\n"
                "**User question / tone/style reference:**\n"
                "{question}\n\n"
                "**STRICT INSTRUCTIONS:**\n"
                "- Acknowledge the code failed with the reported error.\n"
                "- Identify and explain the minimal correction.\n"
                "- Return the **same code back**, identical except for the fixed error.\n"
                "- Do NOT reorder, rewrite, or add anything extra.\n"
                "- Final output must be the corrected, working code."
            ),
        ]
    )
