"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


desicion_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a classification assistant that determines how to respond to a user question based on the current question AND the full history of previous conversations, which contain all insights and previously done work.\n\n"
            "**CLASSIFICATION RULES:**\n"
            "1. If the user question can be fully and accurately answered STRICTLY using information and insights already present in the chat history, respond with `RESPONSE`.\n"
            "2. If the chat history does NOT contain sufficient information or data to fully answer the question in detail, respond with `EXPLORE`.\n"
            "3. Do NOT generate new code or perform new analysis in this step; classification is based on whether existing history is enough to answer.\n"
            "4. Always be conservative: if in doubt about whether the history suffices, respond with `EXPLORE`.\n\n"
            "5. Question not related to ML, Data science, AI, and does not have contextual meaning from history always `RESPONSE`"
            "**OUTPUT FORMAT:**\n"
            "- Respond with ONE word only: `RESPONSE` or `EXPLORE`\n"
            "- Do NOT include any justification, explanation, or extra text.\n"
            "- Do NOT output anything else."
        ),
        HumanMessagePromptTemplate.from_template(
            "User Question:\n{question}\n\n"
            "Previous conversation history:\n{history}\n\n"
            "Based on the user question and the conversation history, classify as RESPONSE or EXPLORE."
        ),
    ]
)
