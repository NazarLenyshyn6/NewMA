"""..."""

from typing import List, Dict

from langchain.prompts import PromptTemplate, FewShotPromptTemplate


class SolutionPlansSummarizationPromptTemplate:
    """..."""

    @staticmethod
    def build(examples: List[Dict[str, str]]) -> FewShotPromptTemplate:
        example_prompt = PromptTemplate(
            input_variables=["summary", "new_solutions", "updated_summary"],
            template=(
                "### EXAMPLE\n"
                "**Existing Global Summary:**\n"
                "{summary}\n\n"
                "**New Solution Plan Steps:**\n"
                "{new_solutions}\n\n"
                "**Updated Global Summary:**\n"
                "{updated_summary}"
            ),
        )

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=(
                "You are an expert ML analysis summarizer responsible for maintaining a **running, evolving summary** of an entire data analysis session.\n\n"
                "Your task is to incrementally refine the global summary each time new solution steps are added. The updated summary must:\n"
                "1. Integrate **all past and new insights** in a unified way (not just repeat the last step).\n"
                "2. Provide a clear **overview of what's been done** and **why** it matters.\n"
                "3. Capture **data-specific insights**, decisions made, and their implications.\n"
                "4. Include **recommendations or next actions** based on the full scope of analysis so far.\n\n"
                "Format should be structured, crisp, and cumulative. Avoid listing step numbers unless meaningful. Focus on key achievements and actionable insights that guide the next move."
            ),
            suffix=(
                "### YOUR TURN\n"
                "**Existing Global Summary:**\n"
                "{summary}\n\n"
                "**New Solution Plan Steps:**\n"
                "{new_solutions}\n\n"
                "**Updated Global Summary:**"
            ),
            input_variables=["summary", "new_solutions"],
        )
