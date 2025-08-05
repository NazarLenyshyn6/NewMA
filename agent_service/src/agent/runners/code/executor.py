"""..."""

from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session

from agent.memory.code.variables import CodeVariablesMemoryManager


class CodeExecutionRunner(BaseModel):
    """..."""

    memory_manager: CodeVariablesMemoryManager

    def execute(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        code: str,
        dependencies: dict,
    ) -> dict:
        """..."""

        variables = self.memory_manager.get_code_variables_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
            storage_uri=storage_uri,
        )

        global_context = dependencies.copy()
        local_context = variables.copy()

        global_context.update(local_context)

        try:
            exec(code, global_context)
            local_context = {
                k: v for k, v in global_context.items() if k not in dependencies
            }
            return local_context

        except Exception as e:
            return f"Exception during code execution: \n{e}"
