"""..."""

from agent.template.summarizers.code.generator import (
    GeneratedCodeSummarizationPromptTemplate,
)
from agent.examples.summarizers.code.generator import (
    generated_code_summarization_examples,
)

generated_code_summarization_prompt = GeneratedCodeSummarizationPromptTemplate.build(
    examples=generated_code_summarization_examples
)
