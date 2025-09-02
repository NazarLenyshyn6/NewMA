"""
This module defines the `FallbackHandlingPrompt` class, which provides a
LangChain `ChatPromptTemplate` for gracefully handling fallback situations
when the model cannot directly answer a user’s question.

The fallback behavior is designed to:
    - Smoothly acknowledge the issue without being abrupt.
    - Remind the user of their original question in varied language.
    - Suggest a natural rephrasing of the question.
    - Ask for confirmation to proceed with the rephrased version.
    - Maintain a conversational, warm, and non-templated style.

This ensures that user experience remains collaborative and natural, even
when direct answers cannot be provided.
"""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


class FallbackHandlingPrompt:
    """Prompt template for gracefully handling fallback responses.

    This class defines a LangChain `ChatPromptTemplate` (UNIFIED) that produces
    conversational, varied fallback responses when the model cannot directly
    answer a user’s question. The fallback ensures a natural user experience by:
        - Acknowledging limitations in varied, polite ways.
        - Restating the original user question with different phrasing.
        - Suggesting a reworded version of the question.
        - Asking for user confirmation to continue with the rephrased version.

    Attributes:
        UNIFIED:
            A fallback prompt that:
                - Acknowledges the issue without being repetitive.
                - References the original user question in varied phrasing.
                - Suggests a natural rewording of the question.
                - Ends by asking the user whether to proceed with the new version.
            The output is conversational, warm, and explicitly non-templated,
            ensuring each response feels collaborative and different.
    """

    UNIFIED: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
You are in **Fallback Mode**.  
Your job is to **gracefully acknowledge the issue** and guide the user forward in a **natural, varied, and non-templated way**.

---

## FALLBACK RESPONSE PRINCIPLES

1. **Smooth Transition**  
   - Continue naturally after the last code attempt.  
   - Avoid sounding repetitive or abrupt.  

2. **Polite + Varied Acknowledgment**  
   - Randomly vary how you express the limitation (e.g., *“Sorry, I couldn’t finish that one…”*, *“Hmm, I can’t give a direct response here…”*, *“That didn’t quite work out…”*).  

3. **Show Original Question**  
   - Remind the user of `{question}`, but vary the phrasing (e.g., *“You asked:”*, *“Your original question was:”*, *“Here’s what you wanted to know:”*).  

4. **Rephrase Naturally**  
   - Suggest a reworded version of `{question}` that preserves meaning.  
   - Vary how you introduce it (e.g., *“Maybe try asking it like this:”*, *“Another way to put it could be:”*).  

5. **Ask User for Confirmation**  
   - End by asking if they’d like to proceed with the rephrased version.  
   - Vary the wording (e.g., *“Want me to run that instead?”*, *“Should I try the new version for you?”*).  

---

## STYLE

- Conversational, collaborative, and warm.  
- **Not robotic, not templated** — must feel different each time.  
- Keep it short, clear, and friendly.
            """
            ),
            HumanMessagePromptTemplate.from_template(
                "User's original question:\n{question}"
            ),
        ]
    )
