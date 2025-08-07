"""..."""

import re
from uuid import UUID
from types import ModuleType
from typing import AsyncGenerator, Optional


from pydantic import BaseModel
from sqlalchemy.orm import Session

from agent.memory.code.variables import CodeVariablesMemoryManager
from agent.code.debagger import CodeDebagger


class CodeExecutionRunner(BaseModel):
    """..."""

    memory_manager: CodeVariablesMemoryManager
    code_debagger: CodeDebagger

    @staticmethod
    def _extract_code(message: str) -> Optional[str]:
        """..."""
        pattern = r"```(?:python)?\n(.*?)(?:\n```)?$"
        match = re.search(pattern, message.strip(), re.DOTALL)

        if not match:
            return None

        return match.group(1).strip()

    async def execute(
        self,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        code: str,
        dependencies: dict,
        current_attempt: int = 1,
        max_attempts: int = 5,
    ):
        if current_attempt > max_attempts:
            yield "Failed"

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
                k: v
                for k, v in global_context.items()
                if k not in dependencies
                and not isinstance(v, ModuleType)
                and not k == "log_step"
            }
            print(local_context.keys())
            yield local_context

        except Exception as e:
            yield "✅"
            print(e)
            print(variables.keys())
            code_fixing_message = []
            async for chunk in self.code_debagger.debug(code, str(e), dependencies):
                code_fixing_message.append(chunk)
                yield chunk

            fixed_code = self._extract_code("".join(code_fixing_message))
            async for result in self.execute(
                db=db,
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
                storage_uri=storage_uri,
                code=fixed_code if fixed_code else code,
                dependencies=dependencies,
                current_attempt=current_attempt + 1,
                max_attempts=max_attempts,
            ):
                yield result
