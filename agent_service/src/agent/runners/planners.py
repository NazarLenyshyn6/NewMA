"""..."""

from typing import Any, List, Dict

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.prompts import ChatPromptTemplate

from agent.planners import SolutionPlanner


class SolutionPlanningRunner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    planners: Dict[str, SolutionPlanner]

    _solutions_planing_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        ...

    def _get_planner(self, input: Dict) -> Dict:
        """..."""
        ...
