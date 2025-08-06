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
#             "You are a senior data scientist and ML engineer skilled in translating technical reports "
#             "into clear, insightful, and business-friendly summaries suitable for stakeholders and users. "
#             "Your task is to read a detailed, step-by-step  report and generate a comprehensive summary that:\n\n"
#             "- Clearly explains what analysis was performed at each step, in simple terms.\n"
#             "- Highlights key findings and their significance or impact on the dataset or downstream analysis.\n"
#             "- Suggests practical next steps, recommendations, or considerations based on the findings.\n\n"
#             "Your summary should be well-structured, easy to understand by non-technical audiences, "
#             "and should convey the importance of the outlier detection results for data quality and analysis decisions.\n"
#             "Use business- and user-oriented language without jargon.\n"
#             "Do not output raw technical data or code; focus on interpretation and implications.\n"
#             "Highlight techical insights and findings"
#             "Format the output as a professional report or executive summary.\n"
#             "**STRICT OUTPUT FORMAT RULES:**\n"
#             "1. Do NOT use markdown formatting (no **, __, *, #, `, etc.).\n"
#             "2. Do NOT include code blocks or backticks.\n"
#             "3. Do NOT use quotation marks, escape sequences, or symbols that would break a Python multiline string.\n"
#             "4. Do NOT include any formatting that would require further post-processing.\n"
#             "5. The entire output must be valid as a raw Python multiline string literal.\n"
#             "6. Only use plain, well-structured text suitable for direct use in string literals.\n\n"
#             "The output must resemble a professional executive summary or analytical report written in plain English."
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "**Detailed Analysis Report:**\n\n{report}\n\n"
#             "Generate a clear, detailed, and user-friendly summary explaining what was done, the key findings and their impact, "
#             "and recommended next steps or actions based on this report."
#         ),
#     ]
# )

template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a senior machine learning engineer and data science communicator. "
            "Your job is to read detailed technical or business reports and produce a short, clear, and highly informative summary.\n\n"
            "**OBJECTIVE:**\n"
            "Create a concise, user-friendly summary that:\n"
            "- Prioritizes key findings and their real-world impact.\n"
            "- Adapts tone: if the report is technical, emphasize technical insights and their implications; "
            "if it's business-focused, summarize in business terms and user outcomes.\n"
            "- Avoids raw data, jargon, or code — focus on the 'what', 'why', and 'so what'.\n"
            "- Is easy to read, well-structured, and directly useful for decisions or next steps.\n\n"
            "**STRICT FORMAT RULES:**\n"
            "1. Do NOT use markdown (*, **, #, `, etc.).\n"
            "2. Do NOT include code blocks, quotes, or escape sequences.\n"
            "3. Use plain, readable English suitable for direct use in Python multiline string literals.\n"
            "4. Output must be short, insightful, and structured like a professional executive summary or update.\n"
            "5. Summary must fit cleanly into frontend UI or chat view — avoid long reports or verbose sections.\n"
            "6. When technical insights are present, center the summary around them with clear explanation.\n"
            "7. When findings are more business/user-facing, highlight outcomes, impact, and recommendations."
        ),
        HumanMessagePromptTemplate.from_template(
            "Here is a detailed report from an analysis:\n\n{report}\n\n"
            "Please summarize it in a clear, concise, and insight-focused way for stakeholders or users, "
            "adapting to the level of technical detail in the report. Keep it short, useful, and to the point."
        ),
    ]
)


reporting_chain = template | anthropic_summary_reporting_model


async def generate_report(report):
    async for chunk in reporting_chain.astream({"report": report}):
        yield chunk.content
