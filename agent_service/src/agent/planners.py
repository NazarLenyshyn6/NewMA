"""..."""

from typing import Any, List
from uuid import UUID
import importlib

from pydantic import BaseModel, ConfigDict, PrivateAttr
from sqlalchemy.orm import Session
from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate

from agent.memory.planners import SolutionPlannerMemoryManager
from agent.dto.dependencies import Dependencies


class SolutionPlanner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate
    memory_manager: SolutionPlannerMemoryManager
    dependencies: List[str]

    _solution_planning_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._solution_planning_chain = self.prompt | self.model

    def generate_solution_plan(
        self,
        question: str,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
    ):
        """..."""
        solutions_history = self.memory_manager.get_solutions_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        print("Solutions history:", solutions_history)
        generated_solution = self._solution_planning_chain.invoke(
            input={"question": question, "history": solutions_history}
        ).content
        return generated_solution

    def get_dependencies(self) -> Dependencies:
        """..."""
        imported_modules = {
            module_name: importlib.import_module(module_name)
            for module_name in self.dependencies
        }
        return Dependencies(
            available_modules=self.dependencies, imported_modules=imported_modules
        )
