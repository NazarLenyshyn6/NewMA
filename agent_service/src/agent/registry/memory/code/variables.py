"""..."""

from agent.memory.code.variables import CodeVariablesMemoryManager
from services.chat_history import chat_history_service

code_variables_memory_manager = CodeVariablesMemoryManager(
    chat_history_service=chat_history_service
)
