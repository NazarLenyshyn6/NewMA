"""..."""

from agent.memory.planners import SolutionPlannerMemoryManager
from services.chat_history import chat_history_service
from agent.registry.summarizers.planners import solution_plans_summarizer

solution_planner_memory_manager = SolutionPlannerMemoryManager(
    chat_history_service=chat_history_service, summarizer=solution_plans_summarizer
)
