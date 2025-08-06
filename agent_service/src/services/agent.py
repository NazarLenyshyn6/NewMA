"""..."""

from uuid import UUID
import re

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

from agent.registry.runners.code.execution import (
    CodeExecutionRunner,
    code_execution_runner,
)

from agent.reporters import generate_report
from agent.registry.memory.planners import solution_planner_memory_manager
from agent.registry.memory.code.variables import code_variables_memory_manager
from agent.registry.memory.code.generator import code_generator_memory_manager
from agent.registry.memory.conversation import conversation_memory_manager


class AgentService(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    task_classification_runner: TasksClassificationRunner
    subtask_classification_runner: SubTasksClassificationRunner
    solution_planning_runner: SolutionPlanningRunner
    code_generation_runner: CodeGenerationRunner
    code_stitching_runner: CodeStitchingRunner
    code_execution_runner: CodeExecutionRunner

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

    async def chat_stream(
        self,
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        dataset_summary: str,
    ):
        # Step 1: Task Classification
        conversation = []
        yield "🧠 Step 1: Task Classification\n"
        yield "🔍 Understanding your question...\n"
        tasks = self.task_classification_runner.classify(question)
        yield f"✅ Identified task(s): `{', '.join(task.lower() for task in tasks)}`\n\n"

        # Step 2: Subtask Classification
        yield "🧠 Step 2: Subtask Classification\n"
        yield "🔍 Breaking down tasks into smaller subtasks...\n"
        subtasks = self.subtask_classification_runner.classify(question, tasks)
        yield f"✅ Subtasks: `{', '.join(subtask.lower() for subtask in subtasks)}`\n\n"

        # Step 3: Solution Planning
        yield "🧠 Step 3: Solution Planning\n"
        yield "🔧 Building a solution strategy...\n"
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
        yield "✅ Solution plan created successfully:\n"
        for i, plan in enumerate(solution_plans, 1):
            yield f"   {i}. {plan}\n"
        yield "\n"

        # Step 4: Code Generation
        yield "🧠 Step 4: Code Generation\n"
        yield "🛠️ Generating code snippets from the plan...\n"
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
        yield f"✅ Generated `{len(code_snippets)}` code snippet(s)\n\n"

        # Step 5: Code Stitching
        yield "🧠 Step 5: Code Stitching\n"
        yield "🧵 Merging code snippets into a complete solution...\n"
        code_chunks = []
        async for chunk in self.code_stitching_runner.stitch_stream(
            question, code_snippets
        ):
            code_chunks.append(chunk)
            yield chunk

        code = "".join(code_chunks)
        yield "\n✅ Code stitching complete.\n\n"

        # Step 6: Code Execution
        yield "🧠 Step 6: Code Execution\n"
        yield "🚀 Running the final code...\n"
        code = re.sub(r"```(?:python)?\n?", "", code).strip()

        variables = None
        async for chunk in self.code_execution_runner.execute(
            db=db,
            session_id=session_id,
            user_id=user_id,
            file_name=file_name,
            storage_uri=storage_uri,
            code=code,
            dependencies=dependencies[0].get_imputed_modules(),
            max_attempts=3,
        ):
            if isinstance(chunk, dict):
                variables = chunk
                break
            if chunk == "Failed":
                break
            yield chunk

        if variables is None:
            yield "Failed."
        else:
            # Extract analysis_report
            yield "\n🧾 Analysis Report:\n"
            analysis_report = variables.get("analysis_report", [])
            formatted_analysis_report = []
            for idx, step in enumerate(analysis_report, 1):
                formatted_analysis_report.append(
                    f"Step {idx}: {step.get('step', '')}\n"
                    f"  Why: {step.get('why', '')}\n"
                    f"  Finding: {step.get('finding', '')}\n"
                    f"  Action: {step.get('action', '')}\n"
                )

            report = "\n".join(formatted_analysis_report)

            async for chunk in generate_report(report):
                conversation.append(chunk)
                yield chunk

            yield "\n\n💾 Updating Agent memory to reflect all plans, analysis insights, and generated code. This ensures consistency for future steps.\n"
            # Save solution plan

            conversation_memory = conversation_memory_manager.get_conversation_history(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            )
            updated_conversation_memory = conversation_memory + [
                {"question": question, "answer": "".join(conversation)}
            ]

            solution_planner_memory_manager.update_solutions_history(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
                new_solutions=report,
            )

            code_variables_memory_manager.update_variables_history(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
                new_code_variables=variables,
            )

            code_generator_memory_manager.update_code_history(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
                new_code=code,
            )
            conversation_memory_manager.update_conversation_history(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
                new_conversation=updated_conversation_memory,
            )
            print(updated_conversation_memory)


agent_service = AgentService(
    task_classification_runner=tasks_classification_runner,
    subtask_classification_runner=subtasks_classification_runner,
    solution_planning_runner=solution_planning_runner,
    code_stitching_runner=code_stitching_runner,
    code_generation_runner=code_generation_runner,
    code_execution_runner=code_execution_runner,
)
