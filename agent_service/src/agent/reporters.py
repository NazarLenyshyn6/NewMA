"""..."""

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

from agent.registry.models.anthropic_ import anthropic_summary_reporting_model


# template = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate.from_template(
#             "You are a senior machine learning engineer and data science communicator. "
#             "Your job is to read detailed technical or business reports and produce a short, clear, and highly informative summary.\n\n"
#             "**OBJECTIVE:**\n"
#             "Create a concise, user-friendly summary that:\n"
#             "- Prioritizes key findings and their real-world impact.\n"
#             "- Adapts tone: if the report is technical, emphasize technical insights and their implications; "
#             "if it's business-focused, summarize in business terms and user outcomes.\n"
#             "- Avoids raw data, jargon, or code — focus on the 'what', 'why', and 'so what'.\n"
#             "- Is easy to read, well-structured, and directly useful for decisions or next steps.\n\n"
#             "**STRICT FORMAT RULES:**\n"
#             "1. Do NOT use markdown (*, **, #, `, etc.).\n"
#             "2. Do NOT include code blocks, quotes, or escape sequences.\n"
#             "3. Use plain, readable English suitable for direct use in Python multiline string literals.\n"
#             "4. Output must be short, insightful, and structured like a professional executive summary or update.\n"
#             "5. Summary must fit cleanly into frontend UI or chat view — avoid long reports or verbose sections.\n"
#             "6. When technical insights are present, center the summary around them with clear explanation.\n"
#             "7. When findings are more business/user-facing, highlight outcomes, impact, and recommendations."
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "Here is a detailed report from an analysis:\n\n{report}\n\n"
#             "Please summarize it in a clear, concise, and insight-focused way for stakeholders or users, "
#             "adapting to the level of technical detail in the report. Keep it short, useful, and to the point."
#         ),
#     ]
# )


# template = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate.from_template(
#             "You are a senior machine learning engineer and data science communicator. "
#             "Your job is to read detailed technical or business reports and produce a short, structured, and highly informative summary.\n\n"
#             "**OBJECTIVE:**\n"
#             "Create a concise, user-friendly summary that:\n"
#             "- Prioritizes key findings and their real-world impact.\n"
#             "- Adapts tone: if the report is technical, emphasize technical insights and their implications; "
#             "if it's business-focused, summarize in business terms and user outcomes.\n"
#             "- Focuses on the 'what', 'why', and 'so what' — no raw data dumps or code.\n"
#             "- Is easy to read, clearly structured, and highly actionable.\n\n"
#             "**STRICT FORMAT AND STYLE REQUIREMENTS:**\n"
#             "1. You MUST use a clean and consistent format throughout the summary.\n"
#             "2. Use **section headers**, **bullet points**, **short paragraphs**, and proper **spacing**.\n"
#             "3. Always include clear headings like: `Key Findings`, `Implications`, `Recommendations`, `Summary`, or similar where appropriate.\n"
#             "4. Be VERY intentional and thoughtful about structure — aim for a great reading experience.\n"
#             "5. Use Markdown formatting (e.g., `**bold**`, `- bullet`, `## Section`) for readability, but NEVER include code blocks, inline code, or quotes.\n"
#             "6. The summary must be brief, deeply insightful, and fit naturally into a frontend UI/chat interface.\n"
#             "7. When technical insights are present, center the summary around them with explanation. "
#             "If business/user-focused, center around value and impact."
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "Here is a detailed report from an analysis:\n\n{report}\n\n"
#             "Please summarize it in a clearly structured, highly readable, and insight-focused way for stakeholders or users. "
#             "Adapt the summary to match the level of technical detail in the original report, and optimize for clarity, usefulness, and format quality."
#         ),
#     ]
# )

template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a senior machine learning engineer and data science communicator. "
            "You are currently assisting a user in generating a summary report from a detailed analysis.\n\n"
            "**OBJECTIVE:**\n"
            "Create a concise, user-friendly summary that:\n"
            "- Prioritizes key findings and their real-world impact.\n"
            "- Adapts tone: if the report is technical, emphasize technical insights and their implications; "
            "if it's business-focused, summarize in business terms and user outcomes.\n"
            "- Focuses on the 'what', 'why', and 'so what' — no raw data dumps or code.\n"
            "- Is easy to read, clearly structured, and highly actionable.\n\n"
            "**STRICT FORMAT AND STYLE REQUIREMENTS:**\n"
            "1. You MUST use a clean and consistent format throughout the summary.\n"
            "2. Use **section headers**, **bullet points**, **short paragraphs**, and proper **spacing**.\n"
            "3. NEVER USER ## formating, replace with any other\n"
            "3. Always include clear headings like: `Key Findings`, `Implications`, `Recommendations`, `Summary`, or similar where appropriate.\n"
            "4. Be VERY intentional and thoughtful about structure — aim for a great reading experience.\n"
            "5. Use Markdown formatting (e.g., `**bold**`, `- bullet`, `## Section`) for readability, but NEVER include code blocks, inline code, or quotes.\n"
            "6. The summary must be brief, deeply insightful, and fit naturally into a frontend UI/chat interface.\n"
            "7. When technical insights are present, center the summary around them with explanation. "
            "If business/user-focused, center around value and impact."
        ),
        HumanMessagePromptTemplate.from_template(
            "Here is a detailed report from an analysis:\n\n{report}\n\n"
            "Please summarize it in a clearly structured, highly readable, and insight-focused way for stakeholders or users. "
            "Adapt the summary to match the level of technical detail in the original report, and optimize for clarity, usefulness, and format quality."
        ),
    ]
)


reporting_chain = template | anthropic_summary_reporting_model


async def generate_report(report):
    async for chunk in reporting_chain.astream({"report": report}):
        yield chunk.content
