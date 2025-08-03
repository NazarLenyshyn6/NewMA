"""..."""

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, PrivateAttr
from sqlalchemy.orm import Session
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate

from agent.memory.code.generator import CodeGeneratorMemoryManager


class CodeGenerator(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate
    memory_manager: CodeGeneratorMemoryManager

    _code_generation_chain: Runnable = PrivateAttr()

    def model_post_init(self, context: Any) -> None:
        """..."""
        self._code_generation_chain = self.prompt | self.model

    def generate_code(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        dependencies: str,
        dataset_summary: str,
        instruction: str,
    ) -> None:
        """..."""
        code_history = self.memory_manager.get_code_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )
        print("Code history:", code_history)
        code = self._code_generation_chain.invoke(
            input={
                "dependencies": dependencies,
                "dataset_summary": dataset_summary,
                "history": code_history,
                "instruction": instruction,
            }
        ).content
        return code
