"""..."""

from agent.memory.planners import SolutionPlannerMemoryManager
from services.chat_history import chat_history_service

solution_planner_memory_manager = SolutionPlannerMemoryManager(
    chat_history_service=chat_history_service
)
