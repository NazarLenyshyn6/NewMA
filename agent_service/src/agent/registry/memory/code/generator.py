"""..."""

from agent.memory.code.generator import CodeGeneratorMemoryManager
from services.chat_history import chat_history_service

code_generator_memory_manager = CodeGeneratorMemoryManager(
    chat_history_service=chat_history_service
)
