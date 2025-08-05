"""..."""

from agent.summarizers.code.generator import GeneratedCodeSummarizer
from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.prompts.summarizers.code.generator import generated_code_summarization_prompt


generated_code_summarizer = GeneratedCodeSummarizer(
    model=anthropic_claude_sonnet_4_20250514_model,
    prompt=generated_code_summarization_prompt,
)
