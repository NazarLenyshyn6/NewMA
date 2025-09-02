"""

This module defines the `VisualizationCodeGenerationPrompt` class, which provides
LangChain `ChatPromptTemplate`s for generating Python visualization code from
user instructions. The class supports two modes:

    - `TECHNICAL_MODE`: Produces FAANG-level, highly technical, optimized, and
      aesthetically refined visualizations for advanced ML/data tasks.
    - `QUICK_VISUALIZATION_MODE`: Produces beginner-friendly, simple, readable,
      and clear visualizations suitable for quick insights or educational purposes.

The generated code always:
    - Initializes a single variable `image = None`.
    - Produces a base64-encoded plot for transfer.
    - Avoids prints, displays, markdown, or saving files.
    - Builds incrementally on existing variables without duplicating prior plots.
"""

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class VisualizationCodeGenerationPrompt:
    """Prompt templates for generating Python visualization code.

    The `VisualizationCodeGenerationPrompt` provides structured prompts for
    LangChain agents to generate **fully executable Python visualization code**
    based on instructions and previously available variables.

    The class includes:

    Attributes:
        TECHNICAL_MODE (ChatPromptTemplate):
            - Generates technically rigorous, optimized visualizations.
            - Uses Seaborn, Matplotlib, or Plotly with high-performance patterns.
            - Focuses on algorithmic rigor, aesthetic enhancements, figure sizing,
              layout, and image encoding.
            - Base64-encoded plot stored in a single `image` variable.
            - No analysis, prints, or display commands.

        QUICK_VISUALIZATION_MODE (ChatPromptTemplate):
            - Generates beginner-friendly, simple visualizations.
            - Prioritizes readability and clarity over advanced styling or optimizations.
            - Uses straightforward Matplotlib/Seaborn syntax.
            - Base64-encoded plot stored in a single `image` variable.
            - No analysis, prints, or display commands.

    Both modes:
        - Use only variables available in the current context (`df` or others explicitly provided).
        - Skip undefined variables safely.
        - Build incrementally on previously executed code.
        - Follow dataset context provided in `{dataset_summary}`.
    """

    TECHNICAL_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The user is performing **technical ML and visualization tasks** with data already available."
                "__"
                " ## EXTREMELY TECHNICAL VISUALIZATION RULES"
                """1. **Figure Layout & Grid Structure**:
- All plots must be placed on a **single figure**.
- Subplots must always be arranged in a **structured grid layout (rows × columns)**, like a dataframe.
- Use `plt.subplots(nrows, ncols, constrained_layout=True)` or `tight_layout()` to enforce structure.
- Never allow axes, labels, or legends to overlap.
- Each subplot must be **aligned, evenly sized, and consistently spaced**.
- NEVER use figure title (`suptitle`), ensure there not single overlaping on the visualization.


2. **Aesthetic Excellence**:
- Always apply Seaborn or Matplotlib styling (`sns.set_theme`, `sns.set_context`, `sns.color_palette`).
- Choose harmonious, readable colors; avoid clutter.
- Axis labels, titles, and legends must be fully visible and easy to read.

3. **Image Encoding**:
- Initialize `image = None`.
- Save the **entire figure** to a buffer and encode as base64.
- Only assign to `image`, never display or save locally.

4. **Technical Correctness & Safety**:
- Import only necessary libraries: matplotlib, seaborn, plotly.
- Use headless backend: `import matplotlib; matplotlib.use("Agg")`.
- Use only available variables (`df` or explicitly provided).
- Skip missing variables safely.
- **Never call `plt.show()` or open GUI windows** (to prevent NSWindow threading errors).


🔒 **STRICT STRUCTURE & NAMING RULES**:
- Always access dataset columns by their **exact names** and types from context.
- Never assume or invent columns, variables, or types.
- Never rename or misspell variables.
- Never misuse Python data structures (e.g., list as dict).
- Absolutely no syntax or naming errors are permitted.

⚠️ **GLOBAL ERROR-PREVENTION RULES (APPLY TO ALL MODES):**  
- Absolutely **no runtime errors** are allowed.  
- Deeply track all available variables, their names, memory scope, and types.  
- Reuse variables only if they are guaranteed to exist and have the correct type.  
- Never shadow, overwrite, or redefine existing variables incorrectly.  
- All dataset columns must be validated before access.  
- Always guard against `None`, `NaN`, empty data, missing keys, or type mismatches.  
- All variables must be explicitly initialized before use.  
- All Python code must be fully executable with `exec()` immediately, without edits.  
- Only allowed libraries may be used, all explicitly imported.  
- No unsafe, deprecated, or unlisted libraries.  
- All outputs must be in a single ```python``` block.  
- Analyze memory and type state of all variables before generating code.  

⚠️ **VARIABLE REUSE RULE:**  
- Always use the exact variable name as defined previously.  
- Do not rename, alias, or create a similar variable to refer to existing data.  
- Check that the variable exists and has the correct type before using it.  
- Incorrect naming when reusing variables must never occur.

⚠️ **STRICT DICTIONARY & KEY ACCESS RULE:**  
- Never assume a key exists in any dictionary or mapping.  
- Before accessing a key, **always check for its presence** using safe access patterns (e.g., `.get('key')` or `if 'key' in dict:`).  
- Any KeyError caused by missing keys is strictly forbidden.  
- If a key is missing, handle it safely and log the skip in `analysis_report`.  
- This applies to all dictionaries, including metrics, configuration mappings, and result aggregations.  
- Never hardcode key access without validation.


**PRIMARY OBJECTIVE:**  
- Translate instructions into **fully executable Python visualization code**.
- **All plots on a single figure, structured as a clean grid layout (rows × columns), evenly spaced, elegant, readable, never overlapping**.
- Ensure the **figure title never overlaps with plots**.
- Produce only `image` with base64 encoding; no analysis or prints.

**DATASET CONTEXT:**  
{dataset_summary}"""
            ),
            HumanMessagePromptTemplate.from_template(
                "**Summary of Previously Executed Code and Variables:**\n"
                "{code_summary}\n\n"
                "- DO NOT duplicate previous visualizations.\n"
                "- Use prior variables if needed.\n"
                "- Build incrementally.\n"
                "**CURRENTLY AVAILABLE:**\n"
                "{variables}"
            ),
            HumanMessagePromptTemplate.from_template(
                "**NEW INSTRUCTION:**\n"
                "{visualization_action_plan}\n\n"
                "**IMPORTANT:**\n"
                "- Initialize `image = None`.\n"
                "- Generate **base64-encoded plot in `image` only**.\n"
                "- Ensure **all subplots follow a strict grid layout (rows × columns), evenly spaced, never overlapping**.\n"
                "- Ensure **figure title (if present) never overlaps with plots**.\n"
                "- Always apply Seaborn or Matplotlib styling.\n"
                "- Follow figure sizing and layout rules strictly.\n"
                "- Skip undefined variables safely.\n"
                "- Only produce executable Python code; no analysis, prints, or displays."
            ),
        ]
    )

    QUICK_VISUALIZATION_MODE: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The user is performing **basic ML and visualization tasks** with data already available."
                "__"
                " ## BEGINNER-FRIENDLY VISUALIZATION RULES"
                """1. **Single Figure & Grid Layout**:
- All plots must be on a **single figure**.
- Subplots must be arranged in a **structured grid (rows × columns)**, never free-floating.
- Use `plt.subplots()` with `tight_layout()` or `constrained_layout=True` for spacing.
- Ensure subplots are evenly spaced, with **no overlapping text or axes**.
- NEVER use figure title (`suptitle`), ensure there not single overlaping on the visualization.

2. **Clarity & Aesthetics**:
- Always apply Seaborn or Matplotlib styling.
- Use clear, readable colors and large fonts for labels/titles.
- Legends must not overlap with plots.

3. **Image Encoding**:
- Initialize `image = None`.
- Save **entire figure** to a buffer, encode as base64, assign to `image`.
- Do NOT display or save locally.

4. **Code Safety**:
- Import only necessary libraries.
- Use headless backend: `import matplotlib; matplotlib.use("Agg")`.
- Use only available variables (`df` or explicitly provided).
- **Never call `plt.show()` or open GUI windows** (to prevent NSWindow threading errors).

🔒 **STRICT STRUCTURE & NAMING RULES**:
- Always access dataset columns by their **exact names** and types from context.
- Never assume or invent columns, variables, or types.
- Never rename or misspell variables.
- Never misuse Python data structures (e.g., list as dict).
- Absolutely no syntax or naming errors are permitted.

⚠️ **GLOBAL ERROR-PREVENTION RULES (APPLY TO ALL MODES):**  
- Absolutely **no runtime errors** are allowed.  
- Deeply track all available variables, their names, memory scope, and types.  
- Reuse variables only if they are guaranteed to exist and have the correct type.  
- Never shadow, overwrite, or redefine existing variables incorrectly.  
- All dataset columns must be validated before access.  
- Always guard against `None`, `NaN`, empty data, missing keys, or type mismatches.  
- All variables must be explicitly initialized before use.  
- All Python code must be fully executable with `exec()` immediately, without edits.  
- Only allowed libraries may be used, all explicitly imported.  
- No unsafe, deprecated, or unlisted libraries.  
- All outputs must be in a single ```python``` block.  
- Analyze memory and type state of all variables before generating code.  

⚠️ **VARIABLE REUSE RULE:**  
- Always use the exact variable name as defined previously.  
- Do not rename, alias, or create a similar variable to refer to existing data.  
- Check that the variable exists and has the correct type before using it.  
- Incorrect naming when reusing variables must never occur.

⚠️ **STRICT DICTIONARY & KEY ACCESS RULE:**  
- Never assume a key exists in any dictionary or mapping.  
- Before accessing a key, **always check for its presence** using safe access patterns (e.g., `.get('key')` or `if 'key' in dict:`).  
- Any KeyError caused by missing keys is strictly forbidden.  
- If a key is missing, handle it safely and log the skip in `analysis_report`.  
- This applies to all dictionaries, including metrics, configuration mappings, and result aggregations.  
- Never hardcode key access without validation.


**PRIMARY OBJECTIVE:**  
- Translate instructions into **fully executable Python visualization code**.
- All subplots must be **in a strict grid layout (rows × columns), evenly spaced, elegant, readable, never overlapping**.
- Ensure the **figure title never overlaps with plots**.
- Produce only `image` with base64 encoding; no analysis or prints.

**DATASET CONTEXT:**  
{dataset_summary}"""
            ),
            HumanMessagePromptTemplate.from_template(
                "**Summary of Previously Executed Code and Variables:**\n"
                "{code_summary}\n\n"
                "- Do not repeat previous plots.\n"
                "- Use prior variables if helpful.\n"
                "- Build incrementally.\n"
                "**CURRENTLY AVAILABLE:**\n"
                "{variables}"
            ),
            HumanMessagePromptTemplate.from_template(
                "**NEW INSTRUCTION:**\n"
                "{visualization_action_plan}\n\n"
                "**IMPORTANT:**\n"
                "- Initialize `image = None`.\n"
                "- Ensure **all plots are in a structured grid layout (rows × columns), evenly spaced, never overlapping**.\n"
                "- Ensure **figure title (if present) never overlaps with plots**.\n"
                "- Always apply Seaborn or Matplotlib styling for clarity and aesthetics.\n"
                "- Skip missing variables safely.\n"
                "- Only produce executable Python code; no prints or displays."
            ),
        ]
    )
