"""..."""

from typing import Any

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.prompts import FewShotPromptTemplate


class GeneratedCodeSummarizer(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: FewShotPromptTemplate

    _solution_plans_summarization_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._solution_plans_summarization_chain = (
            {"summary": RunnablePassthrough(), "generated_code": RunnablePassthrough()}
            | self.prompt
            | self.model
        )

    def summarize(self, summary: str, generated_code: str) -> str:
        """..."""
        return self._solution_plans_summarization_chain.invoke(
            {"summary": summary, "generated_code": generated_code}
        ).content
