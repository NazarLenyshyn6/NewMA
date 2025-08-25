"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class VisualizationCodeGenerationPrompt:
    """..."""

    TECHNICAL_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The user is currently working on **technical machine learning and data visualization tasks** involving data that is **already available** within the system."
                "__"
                " ## EXTREMELY TECHNICAL VISUALIZATION PRINCIPLES (FAANG-TIER)"
                """1. **Algorithmic & Plot Rigor** — Consider data handling and plotting performance:
- Use efficient Python constructs (vectorized Pandas/NumPy, seaborn/matplotlib/plotly idioms).
- Minimize redundant computations, handle large datasets efficiently.
- Ensure all plots are precise, well-aligned, and technically correct.

2. **AESTHETIC ENHANCEMENTS** — Make plots visually striking:
- Prefer Seaborn for styling whenever possible (e.g., `sns.set_theme`, `sns.color_palette`, `sns.set_style`).
- Use vibrant, contrasting, or harmonious color palettes to enhance readability.
- Add meaningful styling: gridlines, context (`sns.set_context`), and figure-wide themes.
- Ensure axis labels, titles, and legends are clearly legible and visually consistent.

3. **IMAGE ENCODING RULE** — Always initialize: image = None.
- Save the figure into a buffer, encode as base64, assign to `image`.
- Do NOT create additional image variables.
- Do NOT display the figure (`plt.show()` forbidden).
- Do NOT save to local files.
- Only transfer-ready base64 `image`.

4. **FIGURE SIZE & LAYOUT RULES** — Ensure plots are clear and visually balanced:
- Large figure size (figsize=(20, 12) or larger).
- For multiple subplots, use `plt.subplots` with even spacing (tight_layout() or `constrained_layout=True`).
- Align images neatly in rows/columns; adjust spacing automatically.

5. **CODE SAFETY & IMPORTS** — Strict control:
- Explicitly import required libraries: matplotlib, seaborn, or plotly.
- Always force headless backend: `import matplotlib; matplotlib.use("Agg")`.
- Do NOT import unlisted libraries.
- Use only variables available in context (e.g., `df`).

**PRIMARY OBJECTIVE:**  
- Translate instructions into **fully executable Python visualization code**.
- Only produce a single `image` variable with base64 encoding.
- Ensure plots are both **technically precise** and **aesthetically stunning**.
- No analysis, no reports, no prints, no display.

**DATASET CONTEXT:**  
{dataset_summary}"""
            ),
            HumanMessagePromptTemplate.from_template(
                "**Summary of Previously Executed Code and Variables:**\n"
                "{code_summary}\n\n"
                "- DO NOT duplicate previous visualizations.\n"
                "- USE prior variables where applicable.\n"
                "- BUILD incrementally on existing data.\n"
                "**CURRENTLY AVAILABLE:**\n"
                "{variables}"
            ),
            HumanMessagePromptTemplate.from_template(
                "**NEW INSTRUCTION:**\n"
                "{visualization_action_plan}\n\n"
                "**IMPORTANT:**\n"
                "- Initialize `image = None`.\n"
                "- Generate base64-encoded plot in `image` only.\n"
                "- Leverage Seaborn styling, vibrant color palettes, and aesthetic enhancements.\n"
                "- Follow **all visualization rules** (figure size, layout, encoding, safety).\n"
                "- Skip undefined variables safely.\n"
                "- Generate only technical Python visualization code — no analysis, no reports, no text output."
            ),
        ]
    )

    QUICK_VISUALIZATION_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The user is currently working on **basic machine learning and data visualization tasks** involving data that is **already available** within the system."
                "__"
                " ## BEGINNER-FRIENDLY VISUALIZATION PRINCIPLES"
                """1. **Simple & Clear Plots** — Focus on readable, easy-to-understand visualizations:
- Use straightforward matplotlib or seaborn syntax.
- Apply Seaborn themes and color palettes where appropriate to enhance visual appeal.
- Avoid overly complex constructs; prioritize clarity.

2. **IMAGE ENCODING RULE** — Always initialize: image = None.
- Save the figure into a buffer, encode as base64, assign to `image`.
- Do NOT create additional variables.
- Do NOT display the figure (`plt.show()` forbidden).
- Do NOT save to local files.
- Only produce `image` for transfer; no text, print, or markdown output.

3. **FIGURE SIZE & LAYOUT RULES** — Ensure clarity:
- Large figure (figsize=(12, 8)).
- Subplots evenly spaced; non-overlapping labels and legends.
- Align neatly in rows/columns; use tight_layout or constrained_layout.

4. **CODE SAFETY & IMPORTS** — Keep safe and simple:
- Import only necessary libraries (matplotlib, seaborn, plotly).
- Use `import matplotlib; matplotlib.use("Agg")` for headless plotting.
- Use only variables provided in context (e.g., `df`).

**PRIMARY OBJECTIVE:**  
- Translate instructions into **fully executable Python visualization code**.
- Only produce a single `image` variable with base64 encoding.
- Generate visually appealing plots leveraging Seaborn styles and palettes.
- No analysis, no reports, no prints, no display. Code must run immediately.

**DATASET CONTEXT:**  
{dataset_summary}"""
            ),
            HumanMessagePromptTemplate.from_template(
                "**Summary of Previously Executed Code and Variables:**\n"
                "{code_summary}\n\n"
                "- DO NOT repeat previous plots.\n"
                "- Use prior variables if helpful.\n"
                "- Build incrementally but keep logic simple.\n"
                "**CURRENTLY AVAILABLE:**\n"
                "{variables}"
            ),
            HumanMessagePromptTemplate.from_template(
                "**NEW INSTRUCTION:**\n"
                "{visualization_action_plan}\n\n"
                "**IMPORTANT:**\n"
                "- Initialize `image = None`.\n"
                "- Generate **base64-encoded plot in `image` only**.\n"
                "- Use Seaborn styling, color palettes, and themes for aesthetic appeal.\n"
                "- Follow all beginner-friendly visualization rules.\n"
                "- Skip safely if a variable is missing.\n"
                "- Only produce executable Python code for visualization; no analysis, reports, prints, or text output."
            ),
        ]
    )
