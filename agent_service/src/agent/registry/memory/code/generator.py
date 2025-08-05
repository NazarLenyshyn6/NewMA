"""..."""

from agent.memory.code.generator import CodeGeneratorMemoryManager
from services.chat_history import chat_history_service
from agent.registry.summarizers.code.generator import generated_code_summarizer

code_generator_memory_manager = CodeGeneratorMemoryManager(
    chat_history_service=chat_history_service, summarizer=generated_code_summarizer
)
