"""..."""

from agent.code.debagger import CodeDebagger
from agent.registry.models.anthropic_ import anthropic_code_stitching_model
from agent.prompts.code.debagger import code_debagging_prompt


code_debagger = CodeDebagger(
    model=anthropic_code_stitching_model, prompt=code_debagging_prompt
)
