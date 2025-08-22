"""..."""

from abc import ABC
from typing import Optional, Any, Type

from pydantic import BaseModel, PrivateAttr, ConfigDict
from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate


from services.memory.base import BaseMemoryService


class BaseNode(ABC, BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate
    output_schema: Optional[Type[BaseModel]] = None
    memory: Optional[BaseMemoryService] = None

    _chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        if self.output_schema is None:
            self._chain = self.prompt | self.model
        else:
            self._chain = self.prompt | self.model.with_structured_output(
                self.output_schema
            )
