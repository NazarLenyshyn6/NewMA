"""..."""

from agent.runners.code.executor import CodeExecutionRunner
from agent.registry.memory.code.variables import code_variables_memory_manager

code_execution_runner = CodeExecutionRunner(
    memory_manager=code_variables_memory_manager
)
