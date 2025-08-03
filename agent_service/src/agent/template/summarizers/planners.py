"""..."""

from typing import List, Dict

from langchain.prompts import PromptTemplate, FewShotPromptTemplate


class SolutionPlansSummarizationPromptTemplate:
    """..."""

    @staticmethod
    def build(examples: List[Dict[str, str]]) -> FewShotPromptTemplate:
        """..."""
        example_prompt = PromptTemplate(
            input_variables=["summary", "new_solutions", "updated_summary"],
            template=(
                "### EXAMPLE\n"
                "Current summary:\n"
                "{summary}\n\n"
                "New lines:\n"
                "{new_solutions}\n\n"
                "New summary:\n"
                "{updated_summary}\n"
            ),
        )

        return FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix=(
                "You are an expert ML assistant responsible for summarizing ML task solution plans.\n"
                "Progressively summarize the solution plan lines by combining them with the existing summary, "
                "returning a concise and updated summary."
            ),
            suffix=(
                "### YOUR TURN\n"
                "Current summary:\n"
                "{summary}\n\n"
                "New lines:\n"
                "{new_solutions}\n\n"
                "New summary:"
            ),
            input_variables=["summary", "new_solutions"],
        )
