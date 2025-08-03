"""..."""

from typing import Any, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, PrivateAttr
from sqlalchemy.orm import Session
from langchain_core.runnables import Runnable, RunnableLambda

from agent.code.generator import CodeGenerator


class CodeGenerationRunner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    code_generator: CodeGenerator

    _code_generation_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._code_generation_chain = RunnableLambda(
            lambda input: self.code_generator.generate_code(**input)
        )

    def generate_code(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        dataset_summary: str,
        instructions: List[str],
        dependencies: List[str],
    ) -> List[str]:
        """..."""
        inputs = [
            {
                "db": db,
                "user_id": user_id,
                "session_id": session_id,
                "file_name": file_name,
                "storage_uri": storage_uri,
                "instruction": instruction,
                "dependencies": dependencies,
                "dataset_summary": dataset_summary,
            }
            for instruction in instructions
        ]
        return self._code_generation_chain.batch(inputs)
