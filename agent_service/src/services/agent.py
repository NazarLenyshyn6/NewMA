"""..."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from sqlalchemy.orm import Session


from agent.registry.runners.classifiers.tasks import (
    TasksClassificationRunner,
    tasks_classification_runner,
)
from agent.registry.runners.classifiers.subtasks import (
    SubTasksClassificationRunner,
    subtasks_classification_runner,
)
from agent.registry.runners.planners import (
    SolutionPlanningRunner,
    solution_planning_runner,
)
from agent.registry.memory.planners import solution_planner_memory_manager


class AgentService(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    task_classification_runner: TasksClassificationRunner
    subtask_classification_runner: SubTasksClassificationRunner
    solution_planning_runner: SolutionPlanningRunner

    def chat(
        self,
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ):
        """..."""
        tasks = self.task_classification_runner.classify(question)
        print("Tasks:", tasks)
        subtasks = self.subtask_classification_runner.classify(question, tasks)
        print("Subtasks:", subtasks)
        solution_plans, dependencies = (
            self.solution_planning_runner.generate_solution_plan(
                question=question,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
                subtasks=subtasks,
            )
        )
        print("Dependencies:", dependencies)

        solution_planner_memory_manager.update_solutions_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
            new_solutions="\n".join(solution_plans),
        )

        return solution_plans


agent_service = AgentService(
    task_classification_runner=tasks_classification_runner,
    subtask_classification_runner=subtasks_classification_runner,
    solution_planning_runner=solution_planning_runner,
)
