"""..."""

from agent.runners.code.generator import CodeGenerationRunner
from agent.registry.code.generator import code_generator

code_generation_runner = CodeGenerationRunner(code_generator=code_generator)
