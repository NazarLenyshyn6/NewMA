"""..."""

from agent.summarizers.planners import SolutionPlansSummarizer
from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.prompts.summarizers.planners import solution_plans_summarization_prompt


solution_plans_summarizer = SolutionPlansSummarizer(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=solution_plans_summarization_prompt,
)
