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

from agent.registry.runners.code.generator import (
    CodeGenerationRunner,
    code_generation_runner,
)

from agent.registry.runners.code.stitcher import (
    CodeStitchingRunner,
    code_stitching_runner,
)

from agent.registry.memory.planners import solution_planner_memory_manager


class AgentService(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    task_classification_runner: TasksClassificationRunner
    subtask_classification_runner: SubTasksClassificationRunner
    solution_planning_runner: SolutionPlanningRunner
    code_generation_runner: CodeGenerationRunner
    code_stitching_runner: CodeStitchingRunner

    def chat(
        self,
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        dataset_summary: str,
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

        print("Solution plan:", solution_plans)

        code_snippets = self.code_generation_runner.generate_code(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
            dataset_summary=dataset_summary,
            instructions=solution_plans,
            dependencies=" ".join(
                [dependency.get_avaliable_modules() for dependency in dependencies]
            ),
        )

        print("Code snippets:", code_snippets)
        if len(code_snippets) == 1:
            return code_snippets[0]

        code = code_stitching_runner.stitch(question, code_snippets)

        return code


agent_service = AgentService(
    task_classification_runner=tasks_classification_runner,
    subtask_classification_runner=subtasks_classification_runner,
    solution_planning_runner=solution_planning_runner,
    code_generation_runner=code_generation_runner,
    code_stitching_runner=code_stitching_runner,
)
