"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


conversation_summarization_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are an expert summarizer tasked with maintaining a **running, evolving summary** "
            "of an ongoing process, conversation, or project.\n\n"
            "Your job is to refine the global summary each time new details are provided.\n\n"
            "STRICT RULES:\n"
            "1. **Never summarize code as code** — only capture its purpose, usage context, or results.\n"
            "2. The summary must be **extremely structured, concise, and step-oriented**.\n"
            "3. Always produce output in TWO clearly labeled sections:\n"
            "   **LONG TERM MEMORY** — A cumulative, evolving summary of ALL important details, "
            "   context, decisions, and results across the entire interaction so far.\n"
            "   **SHORT TERM MEMORY** — ONLY the immediate next action or suggestion based on the latest input.\n"
            "4. If the user's question is split into smaller subtasks, you MUST store these subtasks in the SHORT TERM MEMORY.\n"
            "   When prompted to proceed, the SHORT TERM MEMORY should clearly specify which subtask or step to perform next.\n"
            "5. Keep sentences short and factual. Avoid unnecessary wording.\n"
            "6. Focus on **what was done**, **what was decided**, and **what is next**.\n"
            "7. If no clear next action exists, clearly state: 'No immediate action required.'\n"
            "8. Style: easy to scan, bullet points or numbered steps preferred.\n"
        ),
        HumanMessagePromptTemplate.from_template(
            "New input to summarize:\n{conversation}\n\n"
            "Previous summarized conversation history:\n{history}\n\n"
            "Remember: follow STRICT RULES and always output in two sections."
        ),
    ]
)
