"""..."""

from typing import Any, List

from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable
from langchain.prompts import ChatPromptTemplate


class CodeStitchingRunner(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate

    _code_stitching_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        """..."""
        self._code_stitching_chain = self.prompt | self.model

    @staticmethod
    def _format_code_snippers(code_snippets: List[str]) -> str:
        """..."""
        return "\n\n".join(
            [
                f"Snipped {i}\n: {code_snippet}"
                for i, code_snippet in enumerate(code_snippets, 1)
            ]
        )

    def stitch(self, question: str, code_snippets: List[str]) -> str:
        """..."""
        code = self._code_stitching_chain.invoke(
            {
                "question": question,
                "code_snippets": self._format_code_snippers(code_snippets),
            }
        ).content
        return code
