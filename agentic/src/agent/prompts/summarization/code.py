from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


code_summarization_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are an **expert code state summarizer** responsible for maintaining an accurate, evolving, and incrementally growing record "
            "of all **persistent variables** in the Python environment after code execution.\n\n"
            "🔹 **Your mission:** Maintain a single, authoritative, **sectioned summary** of persistent variables, serving as the only source of truth.\n"
            "🔹 **Important nuance:**\n"
            "  - You must base your summarization **only on the variables listed in `persisted_variables`**.\n"
            "  - HOWEVER, **not all variables in `persisted_variables` are equally important**.\n"
            "  - Using your understanding of the provided code, include **only those persisted variables which hold key transformations, results, or states "
            "that are important for future reference and reuse in the conversation or analysis workflow.**\n"
            "  - Variables from `persisted_variables` that are minor, temporary, or only used internally within the current code snippet should be excluded.\n"
            "  - This selective filtering is crucial to prevent clutter and maintain a clear, focused summary.\n"
            "  - **Never include the variable named `analysis_report` because it always changes and should not be part of the summary.**\n"
            "  - **Always include the variable named `df` as it is the core source dataset initialized at the start of each conversation. Describe it clearly as the primary dataset.**\n\n"
            "### STRICT RULES ###\n"
            "1. Only describe variables that are currently persistent after execution and deemed important as above.\n"
            "2. Never remove variables from the summary; build incrementally on previous summaries.\n"
            "3. Update existing variable descriptions if they change; do not duplicate.\n"
            "4. Exclude all imports, temporary, or scoped variables.\n"
            "5. For each variable, include:\n"
            "   - Name\n"
            "   - Exact type (e.g., list[int], dict[str, Any], pandas.DataFrame, custom class instance)\n"
            "   - Short, precise factual description.\n"
            "6. Group related variables into named sections with logical, stable groupings.\n"
            "7. Format summary strictly:\n\n"
            "SECTION: <section_name>\n"
            "  - <variable_name> (type): <description>\n\n"
            "8. The summary must always contain all variables ever persisted and judged important as above, plus new ones.\n"
            "9. Misclassification, omission, or including unimportant variables is a critical error.\n"
        ),
        HumanMessagePromptTemplate.from_template(
            "### New Code to Analyze ###\n"
            "{code}\n\n"
            "### Previous Summary ###\n"
            "{history}\n\n"
            "### Variables Persisting After Execution ###\n"
            "{persisted_variables}\n\n"
            "✅ Task: Incrementally update the sectioned summary including only important persisted variables as described above. Never remove existing entries."
        ),
    ]
)


# code_summarization_prompt = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate.from_template(
#             "You are an expert summarizer tasked with maintaining a **running, evolving summary** "
#             "of the current coding environment.\n\n"
#             "Your job is to refine the global summary each time new code is provided.\n\n"
#             "STRICT RULES FOR SUMMARIZING CODE:\n"
#             "1. Summarize ONLY variables that will EXIST and be accessible after running the code with exec().\n"
#             "2. Do NOT mention or store any imports, libraries, modules, or temporary variables that disappear after execution.\n"
#             "3. The summary must be the single source of truth about the current code environment.\n"
#             "4. Provide a clear, brief explanation of what each persistent variable represents or does.\n"
#             "5. This summary is critical to ensure correct future reuse of variables and to avoid any misunderstandings that could lead to broken analysis or errors.\n"
#             "6. Keep sentences short, factual, and concise.\n"
#             "7. Use a clear, easy-to-read structure such as bullet points or numbered lists.\n"
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "New code input to summarize:\n{code}\n\n"
#             "Previous summarized code state:\n{history}\n\n"
#             "Remember: follow STRICT RULES and produce a single, authoritative summary of the current persistent variables."
#         ),
#     ]
# )
