"""..."""

from typing import Any, AsyncGenerator

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate


class CodeDebagger(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate

    _code_debagging_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._code_debagging_chain = self.prompt | self.model

    async def debug(
        self, broken_code: str, error_message: str, dependencies: dict
    ) -> AsyncGenerator:
        """..."""
        async for chunk in self._code_debagging_chain.astream(
            {
                "broken_code": broken_code,
                "error_message": error_message,
                "dependencies": ", ".join(
                    dependency for dependency in dependencies.keys()
                ),
            }
        ):
            yield chunk.content
