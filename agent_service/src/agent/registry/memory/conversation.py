"""..."""

from agent.memory.conversation import ConversationMemoryManager
from services.chat_history import chat_history_service

conversation_memory_manager = ConversationMemoryManager(
    chat_history_service=chat_history_service
)
