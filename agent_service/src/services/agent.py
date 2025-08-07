"""..."""

from uuid import UUID
import re
import json

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
from agent.explainers import generate_explanation
from agent.classifiers.flow import FlowClassifier
from agent.registry.classifiers.flow import flow_classifier


class AgentService(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    task_classification_runner: TasksClassificationRunner
    subtask_classification_runner: SubTasksClassificationRunner
    flow_classification_runner: FlowClassifier
    solution_planning_runner: SolutionPlanningRunner
    code_generation_runner: CodeGenerationRunner
    code_stitching_runner: CodeStitchingRunner
    code_execution_runner: CodeExecutionRunner

    @staticmethod
    def format_analysis_report(report):
        def pretty_json(d, indent=4):
            # pretty print dict or list as JSON indented string
            return json.dumps(d, indent=indent, default=str)

        lines = []
        for idx, step in enumerate(report, start=1):
            lines.append(f"Step {idx}: {step.get('step', '')}")
            lines.append(f"  Timestamp: {step.get('timestamp', '')}")
            lines.append(f"  Duration (sec): {step.get('duration_sec', 0):.6f}")
            lines.append(f"  Why: {step.get('why', '')}")

            # Parameters
            parameters = step.get("parameters", {})
            if parameters:
                lines.append("  Parameters:")
                for k, v in parameters.items():
                    lines.append(f"    - {k}: {v}")

            # Inputs
            inputs = step.get("inputs", {})
            if inputs:
                lines.append("  Inputs:")
                for k, v in inputs.items():
                    lines.append(f"    - {k}:")
                    # Format metadata dict pretty but indented further
                    pretty_val = pretty_json(v, indent=6)
                    # indent each line by 6 spaces more
                    for line in pretty_val.splitlines():
                        lines.append(f"      {line}")

            # Outputs
            outputs = step.get("outputs", {})
            if outputs:
                lines.append("  Outputs:")
                for k, v in outputs.items():
                    lines.append(f"    - {k}:")
                    pretty_val = pretty_json(v, indent=6)
                    for line in pretty_val.splitlines():
                        lines.append(f"      {line}")

            # Methodology
            methodology = step.get("methodology", "")
            if methodology:
                lines.append(f"  Methodology: {methodology}")

            # Validation
            validation = step.get("validation", {})
            if validation:
                lines.append("  Validation:")
                pretty_val = pretty_json(validation, indent=4)
                for line in pretty_val.splitlines():
                    lines.append(f"    {line}")

            # Action
            action = step.get("action", "")
            if action:
                lines.append(f"  Action: {action}")

            # Impact
            impact = step.get("impact", {})
            if impact:
                lines.append("  Impact:")
                pretty_val = pretty_json(impact, indent=4)
                for line in pretty_val.splitlines():
                    lines.append(f"    {line}")

            # Branch decision
            branch_decision = step.get("branch_decision", "")
            if branch_decision:
                lines.append(f"  Branch Decision: {branch_decision}")

            lines.append("")  # blank line between steps

        return "\n".join(lines)

    async def executor_stream(
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
        yield "🔍 Understanding your question and intent...\n\n"
        tasks = self.task_classification_runner.classify(question)
        print(tasks)
        yield "✅  \n\n"

        # Step 2: Subtask Classification
        yield "🪜 Step 2: Subtask Classification\n"
        yield "🔧 Decomposing the problem into actionable subtasks...\n\n"
        subtasks = self.subtask_classification_runner.classify(question, tasks)
        print(subtasks)
        yield "✅ \n\n"

        # Step 3: Solution Planning
        yield "🧭 Step 3: Solution Planning\n"
        yield "🧩 Strategizing a path to solve your problem...\n\n"
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
        yield "✅ \n"
        for i, plan in enumerate(solution_plans, 1):
            yield f"   {i}. {plan}\n"
        yield "✅"

        # Step 4: Code Generation
        yield "🛠️ Step 4: Code Generation\n"
        yield "✍️ Writing code snippets based on the plan...\n\n"
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
        yield "✅ \n\n"

        # Step 5: Code Stitching
        yield "🧵 Step 5: Code Assembly\n"
        yield "🧬 Combining snippets into a unified solution...\n\n"
        code_chunks = []
        async for chunk in self.code_stitching_runner.stitch_stream(
            question, code_snippets
        ):
            code_chunks.append(chunk)
            yield chunk

        code = "".join(code_chunks)
        yield "✅ \n\n"

        # Step 6: Code Execution
        yield "🚀 Step 6: Code Execution\n"
        yield "🖥️ Running your code and collecting results...\n\n"
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
            yield "✅ "
            yield "🧾 Step 7: Analysis Report\n"
            yield "🔍 Interpreting results and preparing analysis...\n\n"
            analysis_report = variables.get("analysis_report", [])
            print(analysis_report)
            # formatted_analysis_report = []
            # for idx, step in enumerate(analysis_report, 1):
            # formatted_analysis_report.append(
            #     f"Step {idx}: {step.get('step', '')}\n"
            #     f"  Why: {step.get('why', '')}\n"
            #     f"  Finding: {step.get('finding', '')}\n"
            #     f"  Action: {step.get('action', '')}\n"
            # )

            # report = "\n".join(formatted_analysis_report)
            report = self.format_analysis_report(analysis_report)

            async for chunk in generate_report(report):
                conversation.append(chunk)
                yield chunk

            yield "✅"
            yield "\n📦 Finalizing...\n"
            yield "🧠 Updating Agent memory to retain solution plans, analysis, and generated code for future context.\n\n"
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

    async def explainer_stream(self, question: str, history: str):
        """..."""
        async for chunk in generate_explanation(question=question, history=history):
            yield chunk

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
        flow = self.flow_classification_runner.classify(question)
        conversation = []
        if flow == "EXECUTE":
            async for chunk in self.executor_stream(
                question=question,
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
                dataset_summary=dataset_summary,
            ):
                yield chunk

        elif flow == "EXPLAIN":
            history = solution_planner_memory_manager.get_solutions_history(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
            )
            async for chunk in self.explainer_stream(question, history):
                conversation.append(chunk)
                yield chunk

        else:
            yield "ASK ABOUT ML"

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
        conversation_memory_manager.update_conversation_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
            new_conversation=updated_conversation_memory,
        )


agent_service = AgentService(
    task_classification_runner=tasks_classification_runner,
    subtask_classification_runner=subtasks_classification_runner,
    flow_classification_runner=flow_classifier,
    solution_planning_runner=solution_planning_runner,
    code_stitching_runner=code_stitching_runner,
    code_generation_runner=code_generation_runner,
    code_execution_runner=code_execution_runner,
)
