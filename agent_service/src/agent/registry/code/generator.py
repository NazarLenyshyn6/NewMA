"""..."""

from agent.code.generator import CodeGenerator
from agent.registry.memory.code.generator import code_generator_memory_manager
from agent.registry.models.anthropic_ import anthropic_code_generation_model
from agent.prompts.code.generator import code_generation_prompt

code_generator = CodeGenerator(
    model=anthropic_code_generation_model,
    prompt=code_generation_prompt,
    memory_manager=code_generator_memory_manager,
)
