"""..."""

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)

from agent.registry.models.anthropic_ import anthropic_summary_reporting_model

template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a senior data scientist and ML engineer skilled in translating technical reports "
            "into clear, insightful, and business-friendly summaries suitable for stakeholders and users. "
            "Your task is to read a detailed, step-by-step  report and generate a comprehensive summary that:\n\n"
            "- Clearly explains what analysis was performed at each step, in simple terms.\n"
            "- Highlights key findings and their significance or impact on the dataset or downstream analysis.\n"
            "- Suggests practical next steps, recommendations, or considerations based on the findings.\n\n"
            "Your summary should be well-structured, easy to understand by non-technical audiences, "
            "and should convey the importance of the outlier detection results for data quality and analysis decisions.\n"
            "Use business- and user-oriented language without jargon.\n"
            "Do not output raw technical data or code; focus on interpretation and implications.\n"
            "Highlight techical insights and findings"
            "Format the output as a professional report or executive summary.\n"
            "**STRICT OUTPUT FORMAT REQUIREMENTS:**\n"
            "- Do NOT include any markdown syntax, code blocks, or special formatting.\n"
            "- The output must be directly usable as a Python multiline string literal content without further cleaning.\n"
            "- Avoid any characters or formatting that would break Python string syntax or require additional processing.\n"
        ),
        HumanMessagePromptTemplate.from_template(
            "**Detailed Outlier Analysis Report:**\n\n{report}\n\n"
            "Generate a clear, detailed, and user-friendly summary explaining what was done, the key findings and their impact, "
            "and recommended next steps or actions based on this report."
        ),
    ]
)


reporting_chain = template | anthropic_summary_reporting_model


async def generate_report(report):
    async for chunk in reporting_chain.astream({"report": report}):
        yield chunk.content
