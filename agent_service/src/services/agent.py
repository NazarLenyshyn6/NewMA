"""..."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from sqlalchemy.orm import Session

# from agent_core.task_selectors.builder import TaskSelector, task_selector
# from agent_core.subtask_selectors.builder import SubTaskSelector, sub_task_selector
# from agent_core.solution_planners.builder import SolutionPlanner, solution_planner
from agent.registry.runners.classifiers.tasks import tasks_classification_runner
from agent.registry.runners.classifiers.subtasks import subtasks_classification_runner


class AgentService(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # task_selector: TaskSelector
    # subtask_selector: SubTaskSelector
    # solution_planner: SolutionPlanner

    def invoke(self, question: str, db: Session, session_id: UUID) -> None:
        tasks = tasks_classification_runner.classify(question=question)
        print("Tasks:", tasks)
        subtasks = subtasks_classification_runner.classify(
            qeustion=question, tasks=tasks
        )

        print("Subtasks:", subtasks)
        solution_plans, dependencies = self.solution_planner.generate_solution_plan(
            db=db, session_id=session_id, question=question, subtasks=subtasks
        )
        self.solution_planner.memory_manager.update_solutions_history(
            db=db,
            session_id=session_id,
            question=question,
            new_solutions=solution_plans,
        )
        print("Dependencies:", dependencies)
        return solution_plans


agent_service = AgentService(
    # task_selector=tasks_classification_runner,
    # subtask_selector=subtasks_classification_runner,
    # solution_planner=solution_planner,
)
