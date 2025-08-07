"""..."""

from typing import Any, List


from pydantic import BaseModel, ConfigDict, PrivateAttr
from langchain_core.runnables import Runnable, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage


class FlowClassifier(BaseModel):
    """..."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: Runnable
    prompt: ChatPromptTemplate

    _flow_classifcation_chain: Runnable = PrivateAttr()

    def model_post_init(self, __context: Any) -> None:
        self._flow_classifcation_chain = self.prompt | self.model

    def classify(self, question: str) -> str:
        flow = self._flow_classifcation_chain.invoke({"question": question})
        return flow.content
