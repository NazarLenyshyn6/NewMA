"""..."""

from typing import Any, List, Dict, Tuple
from uuid import UUID

from pydantic import BaseModel, ConfigDict, PrivateAttr
from sqlalchemy.orm import Session
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.prompts import ChatPromptTemplate

from agent.planners import SolutionPlanner
from agent.dto.dependencies import Dependencies


class SolutionPlanningRunner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    planners: Dict[str, SolutionPlanner]

    _solutions_planing_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._solutions_planing_chain = RunnableLambda(
            lambda input: self._get_planner(input)
        ) | RunnableLambda(lambda input: self._generate_solution_plan(input))

    def _get_planner(self, input: Dict) -> Dict:
        """..."""
        subtask = input.get("subtask")
        input.pop("subtask")
        planner = self.planners.get(subtask)
        if planner is None:
            raise
        input["planner"] = planner
        return input

    def _generate_solution_plan(self, input: Dict) -> Tuple[str, Dependencies]:
        """..."""
        planner: SolutionPlanner = input.get("planner")
        input.pop("planner")
        solution_plan = planner.generate_solution_plan(**input)
        return solution_plan, planner.get_dependencies()

    def generate_solution_plan(
        self,
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        subtasks: List[str],
    ) -> Tuple[List[str], List[Dependencies]]:
        """..."""
        inputs = [
            {
                "question": question,
                "db": db,
                "user_id": user_id,
                "session_id": session_id,
                "file_name": file_name,
                "storage_uri": storage_uri,
                "subtask": subtask,
            }
            for subtask in subtasks
        ]
        responses = self._solutions_planing_chain.batch(inputs)
        solution_plans = [response[0] for response in responses]
        dependencies = [response[1] for response in responses]
        return solution_plans, dependencies
