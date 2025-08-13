"""..."""

from abc import ABC, abstractmethod
from typing import Any, Optional, List
from uuid import UUID

from pydantic import BaseModel, PrivateAttr, ConfigDict
from sqlalchemy.orm import Session
from langchain_core.runnables import Runnable, RunnableParallel
from langchain.prompts import ChatPromptTemplate

from services.memory import AgentMemoryService


class BaseNode(BaseModel, ABC):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Optional[Runnable] = None
    prompt: Optional[ChatPromptTemplate] = None
    memory: Optional[AgentMemoryService] = None

    _token_buffer: list = PrivateAttr(default_factory=list)
    _chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        if self.prompt is not None and self.model is not None:
            self._chain = self.prompt | self.model
        else:
            self._chain = None

    @abstractmethod
    def run(
        self,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
        *args,
        **kwargs
    ):
        """..."""
        ...

    @abstractmethod
    def arun(
        self,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
        *args,
        **kwargs
    ):
        """..."""
        ...

    def get_steamed_tokens(self) -> str:
        return "".join(self._token_buffer)


class BaseParallelNode(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    memory: AgentMemoryService

    @abstractmethod
    def run(
        self,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
        *args,
        **kwargs
    ):
        """..."""
        ...
