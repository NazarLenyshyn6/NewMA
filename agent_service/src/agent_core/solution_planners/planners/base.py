"""..."""

from uuid import UUID
from typing import Any, List
import importlib

from pydantic import BaseModel, ConfigDict, PrivateAttr
from sqlalchemy.orm import Session
from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate

from agent_core.solution_planners.memory import SolutionsMemoryManager
from agent_core.solution_planners.dto import Dependencies


class BaseSolutionPlanner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt_template: ChatPromptTemplate
    memory_manager: SolutionsMemoryManager
    dependencies: List[str]

    _plan_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._plan_chain = self.prompt_template | self.model

    def generate_solution_plan(
        self, db: Session, session_id: UUID, question: str
    ) -> str:
        """..."""
        history = self.memory_manager.get_solutions_history(
            db=db, session_id=session_id
        )
        print(f"HISTORY: {len(history)}")
        response = self._plan_chain.invoke(
            input={"question": question, "history": history}
        ).content
        return response

    def import_dependencies(self) -> Dependencies:
        """
        Dynamically import and return required modules.
        """
        imported_modules = {
            module_name: importlib.import_module(module_name)
            for module_name in self.dependencies
        }
        return Dependencies(
            available_modules=self.dependencies, imported_modules=imported_modules
        )
