"""..."""

from agent.template.summarizers.planners import SolutionPlansSummarizationPromptTemplate
from agent.examples.summarizers.planners import solution_plans_summarization_examples

solution_plans_summarization_prompt = SolutionPlansSummarizationPromptTemplate.build(
    examples=solution_plans_summarization_examples
)
