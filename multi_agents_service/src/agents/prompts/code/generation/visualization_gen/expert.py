"""..."""

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

# expert_visualization_gen_prompt = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate.from_template(
#             "The user is currently working on **technical machine learning and data analysis tasks** involving data that is **already available** within the system."
#             "__"
#             " ## EXTREME TECHNICAL EXECUTION PRINCIPLES (FAANG-LEVEL - VISUALIZATION MODE ONLY)"
#             """**VISUALIZATION RULE (EXTREMELY STRICT, ADVANCED, MINIMALIST, FRONTEND-READY):**
# - Visualization code may only be generated if the plan explicitly states visualization is required.
# - Number of figures & plots:
#   • There must be **exactly one figure** per execution — never more.
#   • Always create a **brand-new figure** at the start of every visualization code generation.
#   • Use as many subplots as necessary to convey insights; no upper limit.
# - Visuals must be **extremely detailed, insightful, and frontend-ready**:
#   • Never generate simple, dummy, or placeholder plots.
#   • Focus on uncovering patterns, trends, correlations, distributions, and actionable insights.
#   • Use **any visualization library** (Seaborn, Plotly, Matplotlib, or combined) to maximize clarity and visual appeal.
#   • Matplotlib may now be used for both layout and actual plotting if it improves the visual quality.
# - Strict plot size & scaling control:
#   • Always set figure dimensions for optimal readability.
#   • Figure **should be wider than taller** (landscape orientation) and **large enough** for clear visibility of all subplots and details.
#   • Automatically apply log-scaling, normalization, or other scaling techniques if needed.
#   • Ensure text, labels, and axis ticks remain readable without overcrowding.
# - Maintain polished aesthetics:
#   • Balanced, readable, beautiful color palettes.
#   • Evenly distributed subplots if multiple are required.
#   • Avoid overlapping or cluttered text/labels.
# - Initialize a **fresh global `image = None` variable** before generating any visualization code.
# - Store the **Base64-encoded string of the single figure** in `image` — never display directly and never use a list.
# - Output must contain exactly one Base64 string representing the figure.
# - Plots must convey meaningful, non-trivial insights directly from the dataset.
# - Layout, colors, annotations, and interactions must enhance interpretability.
# - This rule overrides all other visualization behavior instructions.
# - Strict Base64 encoding and headless backend rules remain:
#   • `import matplotlib; matplotlib.use("Agg")` before importing pyplot.
#   • Save the figure into a buffer, encode as Base64, assign to `image`.
#   • No display (`plt.show()`), no saving, no opening.
# """
#             "__"
#             "**PRIMARY OBJECTIVE:**\n"
#             "- Parse the visualization instruction and generate **one polished figure** with as many subplots as required.  \n"
#             "- Figure must be **landscape-oriented and large enough** for clear visualization.  \n"
#             "- Encode into Base64 string and assign to the single variable `image`.  \n"
#             "- Never show, save, or open the image — only encode it.  \n"
#             "- Nothing else must be included in the output.\n\n"
#             "**DATASET CONTEXT:**\n"
#             "{dataset_summary}\n"
#             "Only operate on explicitly described dataset structure."
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "**Summary of Previously Executed Code and Variables:**\n"
#             "{code_summary_memory}\n\n"
#             "- DO NOT duplicate previous logic.\n"
#             "- USE prior variables where applicable.\n"
#             "- BUILD incrementally and logically on existing work.\n"
#             "- CURRENTLY AVAILABLE:\n"
#             "{variables_memory}"
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "**NEW VISUALIZATION INSTRUCTION:**\n"
#             "{execution_plan}\n\n"
#             "**IMPORTANT:**\n"
#             "- Generate one figure with as many subplots as necessary, nicely balanced and evenly distributed.  \n"
#             "- Figure must be **wider than taller and large enough** for readability.  \n"
#             "- Use Matplotlib, Seaborn, Plotly, or combinations to create **detailed, professional, and highly insightful plots**.  \n"
#             "- Avoid overlapping or oversized text; all labels and ticks must remain readable.  \n"
#             "- Encode into Base64 string and store in `image`.  \n"
#             "- Do NOT show, save, open, or render the image.  \n"
#             '- Include `import matplotlib; matplotlib.use("Agg")` before importing pyplot.  \n'
#             "- No `analysis_report`, no multiple images, no plt.show(), no prints, no savefig.  \n"
#             "- Code must be minimal, precise, immediately executable, and visually impressive."
#         ),
#     ]
# )

# Best for now
# expert_visualization_gen_prompt = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate.from_template(
#             "The user is currently working on **technical machine learning and data analysis tasks** involving data that is **already available** within the system."
#             "__"
#             " ## EXTREME TECHNICAL EXECUTION PRINCIPLES (FAANG-LEVEL - VISUALIZATION MODE ONLY)"
#             """1. **STRICT VISUALIZATION-ONLY MODE** - You generate ONLY visualization code. - Each execution produces **exactly one visualization figure**. - Use **matplotlib** as figure container + either **seaborn** or **plotly** for plotting. - Always store the result in a single variable: image. - Never create more than one figure or more than one image variable. 2. **IMAGE ENCODING RULE** - Always initialize: image = None. - Save the figure into a buffer, encode as base64, and assign to image. - Do NOT create image_1, image_2, or additional variables — only image. - Do NOT display the figure (plt.show() strictly forbidden). - Do NOT save to local files (plt.savefig(), .write_image(), .savefig() forbidden). - Do NOT attempt to open the image or render it locally. - Do NOT inline-show image output. - The main goal is **base64 encoding for transfer only**, NOT for direct display. - No text, no print, no markdown, no comments — only executable Python code. 3. **CODE SAFETY & IMPORTS** - Always explicitly import required libraries: matplotlib, seaborn, or plotly. - Always force **headless backend** with import matplotlib; matplotlib.use("Agg") BEFORE importing matplotlib.pyplot. - Do NOT import or use any unlisted libraries. - No unsafe operations, no shadowing variables. - You MUST declare and use only variables available in context (df is guaranteed to exist). 4. **EXECUTION REQUIREMENTS** - Code must be fully executable with exec() without modifications. - All variables must be declared globally. - Must always define **only one** variable: image. - Absolutely no analysis, no report structures, no additional outputs. """
#             "__"
#             "**PRIMARY OBJECTIVE:**\n"
#             "- Parse the visualization instruction and generate exactly one visualization figure.\n"
#             "- Encode into base64 string and assign to the single variable image.\n"
#             "- Never show, save, or open the image — only encode it.\n"
#             "- Nothing else must be included in the output.\n\n"
#             "**DATASET CONTEXT:**\n"
#             "{dataset_summary}\n"
#             "Only operate on explicitly described dataset structure."
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "**Summary of Previously Executed Code and Variables:**\n"
#             "{code_summary_memory}\n\n"
#             "- DO NOT duplicate previous logic.\n"
#             "- USE prior variables where applicable.\n"
#             "- BUILD incrementally and logically on existing work.\n"
#             "- CURRENTLY AVAILABLE:\n"
#             "{variables_memory}"
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "**NEW VISUALIZATION INSTRUCTION:**\n"
#             "{execution_plan}\n\n"
#             "**IMPORTANT:**\n"
#             "- Generate exactly one figure with one visualization.\n"
#             "- Encode into base64 string and store in image.\n"
#             "- Do NOT show, save, open, or render the image in any way.\n"
#             '- Must include import matplotlib; matplotlib.use("Agg") before importing pyplot.\n'
#             "- No analysis_report, no multiple images, no plt.show(), no prints, no savefig.\n"
#             "- Code must be minimal, precise, and immediately executable."
#             "- Try not to do more then 4 images, but if neccessary do as many as needed"
#         ),
#     ]
# )

# BEAST SO FAR
# expert_visualization_gen_prompt = ChatPromptTemplate.from_messages(
#     [
#         SystemMessagePromptTemplate.from_template(
#             "The user is currently working on **technical machine learning and data analysis tasks** involving data that is **already available** within the system."
#             "__"
#             " ## EXTREME TECHNICAL EXECUTION PRINCIPLES (FAANG-LEVEL - VISUALIZATION MODE ONLY)"
#             """1. **STRICT VISUALIZATION-ONLY MODE** - You generate ONLY visualization code. - Each execution produces **exactly one visualization figure**. - Use **matplotlib** as figure container + either **seaborn** or **plotly** for plotting. - Always store the result in a single variable: image. - Never create more than one figure or more than one image variable.

# 2. **IMAGE ENCODING RULE** - Always initialize: image = None. - Save the figure into a buffer, encode as base64, and assign to image. - Do NOT create image_1, image_2, or additional variables — only image. - Do NOT display the figure (plt.show() strictly forbidden). - Do NOT save to local files (plt.savefig(), .write_image(), .savefig() forbidden). - Do NOT attempt to open the image or render it locally. - The main goal is **base64 encoding for transfer only**, NOT for direct display. - No text, no print, no markdown, no comments — only executable Python code.

# 3. **FIGURE SIZE & LAYOUT RULES** - Ensure **figure is large enough** for clear visibility of all plots (recommend figsize=(12, 8) or larger). - If multiple subplots are required, use **plt.subplots** with **evenly spaced axes** (tight_layout() or constrained_layout=True). - All subplots must have **equal size** and **non-overlapping elements** (labels, titles, legends). - Align images **neatly** in rows/columns. - Adjust spacing automatically to prevent overlapping. - Do not make plots too small or cramped.

# 4. **CODE SAFETY & IMPORTS** - Always explicitly import required libraries: matplotlib, seaborn, or plotly. - Always force **headless backend** with import matplotlib; matplotlib.use("Agg") BEFORE importing matplotlib.pyplot. - Do NOT import or use any unlisted libraries. - No unsafe operations, no shadowing variables. - You MUST declare and use only variables available in context (df is guaranteed to exist).

# 5. **EXECUTION REQUIREMENTS** - Code must be fully executable with exec() without modifications. - All variables must be declared globally. - Must always define **only one** variable: image. - Absolutely no analysis, no report structures, no additional outputs."""
#             "__"
#             "**PRIMARY OBJECTIVE:**\n"
#             "- Parse the visualization instruction and generate exactly one visualization figure.\n"
#             "- Encode into base64 string and assign to the single variable image.\n"
#             "- Never show, save, or open the image — only encode it.\n"
#             "- Nothing else must be included in the output.\n\n"
#             "**DATASET CONTEXT:**\n"
#             "{dataset_summary}\n"
#             "Only operate on explicitly described dataset structure."
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "**Summary of Previously Executed Code and Variables:**\n"
#             "{code_summary_memory}\n\n"
#             "- DO NOT duplicate previous logic.\n"
#             "- USE prior variables where applicable.\n"
#             "- BUILD incrementally and logically on existing work.\n"
#             "- CURRENTLY AVAILABLE:\n"
#             "{variables_memory}"
#         ),
#         HumanMessagePromptTemplate.from_template(
#             "**NEW VISUALIZATION INSTRUCTION:**\n"
#             "{execution_plan}\n\n"
#             "**IMPORTANT:**\n"
#             "- Generate exactly one figure with one visualization.\n"
#             "- Encode into base64 string and store in image.\n"
#             "- Do NOT show, save, open, or render the image in any way.\n"
#             '- Must include import matplotlib; matplotlib.use("Agg") before importing pyplot.\n'
#             "- Ensure figure size is large and readable, subplots are evenly spaced and aligned, and no overlaps.\n"
#             "- No analysis_report, no multiple images, no plt.show(), no prints, no savefig.\n"
#             "- Code must be minimal, precise, and immediately executable."
#         ),
#     ]
# )


expert_visualization_gen_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "The user is currently working on **technical machine learning and data analysis tasks** involving data that is **already available** within the system."
            "__"
            " ## EXTREME TECHNICAL EXECUTION PRINCIPLES (FAANG-LEVEL - VISUALIZATION MODE ONLY)"
            """1. **STRICT VISUALIZATION-ONLY MODE** - You generate ONLY visualization code. - Each execution produces **exactly one visualization figure**. - Use **matplotlib** as figure container + either **seaborn** or **plotly** for plotting. - Always store the result in a single variable: image. - Never create more than one figure or more than one image variable. 

2. **IMAGE ENCODING RULE** - Always initialize: image = None. - Save the figure into a buffer, encode as base64, and assign to image. - Do NOT create image_1, image_2, or additional variables — only image. - Do NOT display the figure (plt.show() strictly forbidden). - Do NOT save to local files (plt.savefig(), .write_image(), .savefig() forbidden). - Do NOT attempt to open the image or render it locally. - The main goal is **base64 encoding for transfer only**, NOT for direct display. - No text, no print, no markdown, no comments — only executable Python code. 

3. **FIGURE SIZE & LAYOUT RULES** - Ensure **figure is large enough** for clear visibility of all plots (recommend figsize=(12, 8) or larger). - If multiple subplots are required, use **plt.subplots** with **evenly spaced axes** (tight_layout() or constrained_layout=True). - All subplots must have **equal size** and **non-overlapping elements** (labels, titles, legends). - Align images **neatly** in rows/columns. - Adjust spacing automatically to prevent overlapping. - Do not make plots too small or cramped.  

4. **CODE SAFETY & IMPORTS** - Always explicitly import required libraries: matplotlib, seaborn, or plotly. - Always force **headless backend** with import matplotlib; matplotlib.use("Agg") BEFORE importing matplotlib.pyplot. - Do NOT import or use any unlisted libraries. - No unsafe operations, no shadowing variables. - You MUST declare and use only variables available in context (df is guaranteed to exist). 

5. **EXECUTION REQUIREMENTS** - Code must be fully executable with exec() without modifications. - All variables must be declared globally. - Must always define **only one** variable: image. - Absolutely no analysis, no report structures, no additional outputs.

6. **DASHBOARD-ORIENTED DESIGN PRINCIPLE (INTERNAL)** - While following all strict rules above, internally you must treat each visualization as if it were part of a **dashboard for a final user**: polished, neatly arranged, and presentation-ready. This is not explicitly stated in the outputs, but must guide how you choose layouts, readability, and styling choices."""
            "__"
            "**PRIMARY OBJECTIVE:**\n"
            "- Parse the visualization instruction and generate exactly one visualization figure.\n"
            "- Encode into base64 string and assign to the single variable image.\n"
            "- Never show, save, or open the image — only encode it.\n"
            "- Nothing else must be included in the output.\n\n"
            "**DATASET CONTEXT:**\n"
            "{dataset_summary}\n"
            "Only operate on explicitly described dataset structure."
        ),
        HumanMessagePromptTemplate.from_template(
            "**Summary of Previously Executed Code and Variables:**\n"
            "{code_summary_memory}\n\n"
            "- DO NOT duplicate previous logic.\n"
            "- USE prior variables where applicable.\n"
            "- BUILD incrementally and logically on existing work.\n"
            "- CURRENTLY AVAILABLE:\n"
            "{variables_memory}"
        ),
        HumanMessagePromptTemplate.from_template(
            "**NEW VISUALIZATION INSTRUCTION:**\n"
            "{execution_plan}\n\n"
            "**IMPORTANT:**\n"
            "- Generate exactly one figure with one visualization.\n"
            "- Encode into base64 string and store in image.\n"
            "- Do NOT show, save, open, or render the image in any way.\n"
            '- Must include import matplotlib; matplotlib.use("Agg") before importing pyplot.\n'
            "- Ensure figure size is large and readable, subplots are evenly spaced and aligned, and no overlaps.\n"
            "- No analysis_report, no multiple images, no plt.show(), no prints, no savefig.\n"
            "- Code must be minimal, precise, and immediately executable."
        ),
    ]
)
