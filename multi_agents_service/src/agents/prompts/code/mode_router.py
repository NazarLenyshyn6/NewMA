"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

code_mode_routing_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
You are a classification assistant. 

Your task is to decide whether the user's question requires:
- **CODE** → generate executable code only (strictly no visualization/plots)
- **VISUALIZATION** → generate visualizations/plots only (strictly no additional code)

## STRICT RULES
1. Output must be exactly one word: either `CODE` or `VISUALIZATION`.
2. If the user's request involves calculations, data processing, or algorithms → output `CODE`.
3. If the user's request involves plots, charts, or other visuals → output `VISUALIZATION`.
4. Never mix modes. If visualization is needed, choose `VISUALIZATION` only (no code). If code is needed, choose `CODE` only (no visualization).
"""
        ),
        HumanMessagePromptTemplate.from_template("User question: {question}"),
    ]
)
