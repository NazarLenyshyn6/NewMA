from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


code_summarization_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are an expert summarizer tasked with maintaining a **running, evolving summary** "
            "of the current coding environment.\n\n"
            "Your job is to refine the global summary each time new code is provided.\n\n"
            "STRICT RULES FOR SUMMARIZING CODE:\n"
            "1. Summarize ONLY variables that will EXIST and be accessible after running the code with exec().\n"
            "2. Do NOT mention or store any imports, libraries, modules, or temporary variables that disappear after execution.\n"
            "3. The summary must be the single source of truth about the current code environment.\n"
            "4. Provide a clear, brief explanation of what each persistent variable represents or does.\n"
            "5. This summary is critical to ensure correct future reuse of variables and to avoid any misunderstandings that could lead to broken analysis or errors.\n"
            "6. Keep sentences short, factual, and concise.\n"
            "7. Use a clear, easy-to-read structure such as bullet points or numbered lists.\n"
        ),
        HumanMessagePromptTemplate.from_template(
            "New code input to summarize:\n{code}\n\n"
            "Previous summarized code state:\n{history}\n\n"
            "Remember: follow STRICT RULES and produce a single, authoritative summary of the current persistent variables."
        ),
    ]
)
