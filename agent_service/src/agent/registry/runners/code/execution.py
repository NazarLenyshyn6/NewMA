"""..."""

from agent.runners.code.executor import CodeExecutionRunner
from agent.registry.memory.code.variables import code_variables_memory_manager
from agent.registry.code.debagger import code_debagger

code_execution_runner = CodeExecutionRunner(
    memory_manager=code_variables_memory_manager, code_debagger=code_debagger
)
