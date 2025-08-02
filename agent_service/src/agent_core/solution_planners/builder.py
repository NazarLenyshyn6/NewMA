"""..."""

from uuid import UUID
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel, ConfigDict, PrivateAttr
from sqlalchemy.orm import Session
from langchain_core.runnables import Runnable, RunnableLambda


from agent_core.subtask_selectors.enums.base import BaseSubTask
from agent_core.subtask_selectors.enums.eda import EdaSubTask
from agent_core.subtask_selectors.enums.classification import ClassificationSubTask
from agent_core.solution_planners.planners.base import BaseSolutionPlanner
from agent_core.solution_planners.planners import eda as eda_planners
from agent_core.solution_planners.dto import Dependencies
from agent_core.solution_planners.memory import (
    SolutionsMemoryManager,
    solutions_memory_manager,
)
from agent_core.solution_planners.planners import (
    classification as classification_planners,
)


class SolutionPlanner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    solution_planners: Dict[str, BaseSolutionPlanner]
    memory_manager: SolutionsMemoryManager

    _plan_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._plan_chain = RunnableLambda(
            lambda input: self._get_solution_planner(input=input)
        ) | RunnableLambda(lambda input: self._execute_solution_planner(input=input))

    def _get_solution_planner(self, input: dict) -> dict:
        """..."""
        subtask = input.get("subtask")
        if subtask is None:
            raise
        solution_planner = self.solution_planners.get(subtask)
        if solution_planner is None:
            raise
        input["solution_planner"] = solution_planner
        return input

    def _execute_solution_planner(self, input: dict) -> Tuple[str, Dependencies]:
        """..."""
        solution_planner: BaseSolutionPlanner = input.get("solution_planner")
        solution_plan = solution_planner.generate_solution_plan(
            db=input["db"], session_id=input["session_id"], question=input["question"]
        )
        return (solution_plan, solution_planner.import_dependencies())

    def generate_solution_plan(
        self, db: Session, session_id: UUID, question: str, subtasks: List[str]
    ) -> Tuple[List[str], List[Dependencies]]:
        """..."""
        inputs = [
            {
                "question": question,
                "session_id": session_id,
                "db": db,
                "subtask": subtask,
            }
            for subtask in subtasks
        ]
        response = self._plan_chain.batch(inputs=inputs)
        solution_plans = [r[0] for r in response]
        dependencies = [r[1] for r in response]
        return (solution_plans, dependencies)


solution_planners = {
    EdaSubTask.MISSING_VALUES.name: eda_planners.missing_values_solution_planner,
    EdaSubTask.DUPLICATE_ROWS_DETECTION.name: eda_planners.duplicate_rows_detection_solution_planner,
    EdaSubTask.DATA_TYPES_CHECK.name: eda_planners.data_types_check_solution_planner,
    EdaSubTask.UNIQUE_VALUES_ANALYSIS.name: eda_planners.unique_values_analysis_solution_planner,
    EdaSubTask.STATISTICAL_SUMMARY.name: eda_planners.statistical_summary_solution_planner,
    EdaSubTask.DISTRIBUTION_ANALYSIS.name: eda_planners.distribution_analysis_solution_planner,
    EdaSubTask.OUTLIER_DETECTION.name: eda_planners.outlier_detection_solution_planner,
    EdaSubTask.CORRELATION_ANALYSIS.name: eda_planners.correlation_analysis_solution_planner,
    EdaSubTask.PAIR_PLOTS.name: eda_planners.pair_plots_solution_planner,
    EdaSubTask.CATEGORICAL_VS_TARGET.name: eda_planners.categorical_vs_target_solution_planner,
    EdaSubTask.NUMERICAL_VS_TARGET.name: eda_planners.numerical_vs_target_solution_planner,
    EdaSubTask.MISSING_VALUE_IMPUTATION_STRATEGY.name: eda_planners.missing_value_imputation_strategy_solution_planner,
    EdaSubTask.CLASS_DISTRIBUTION_CHECK.name: eda_planners.class_distribution_check_solution_planner,
    EdaSubTask.HEATMAPS.name: eda_planners.heatmaps_solution_planner,
    EdaSubTask.TIME_SERIES_ANALYSIS.name: eda_planners.time_series_analysis_solution_planner,
    EdaSubTask.DATA_PROVENANCE_CHECK.name: eda_planners.data_provenance_check_solution_planner,
    EdaSubTask.LOG_TRANSFORMATION_CHECK.name: eda_planners.log_transformation_check_solution_planner,
    EdaSubTask.DATA_COMPLETENESS_CHECK.name: eda_planners.data_completeness_check_solution_planner,
}

solution_planner = SolutionPlanner(
    solution_planners=solution_planners, memory_manager=solutions_memory_manager
)
