"""..."""

import pickle

from agents.nodes.base import BaseNode
from agents.prompts.request_router import request_routing_prompt
from agents.models.anthropic_ import request_routing_model
from agents.state import AgentState
from services.memory.conversation_summary import conversation_summary_memory_service


class RequestRouterNode(BaseNode):

    def route(self, state: AgentState) -> AgentState:
        """..."""
        print("* RequestRouterNode -> ")

        # Retviever conversation summary memoryt and store in graph state, to avoid unvessesary retriving from cache
        state.conversation_summary_memory = pickle.loads(
            conversation_summary_memory_service.get_memory(
                db=state.db,
                user_id=state.user_id,
                session_id=state.session_id,
                file_name=state.file_name,
                storage_uri=state.storage_uri,
            ).memory
        )
        state.request_type = self._chain.invoke(
            {
                "question": state.question,
                "conversation_summary_memory": state.conversation_summary_memory,
            },
            config={"metadata": {"stream": False}},
        ).content

        # Add question to conversation memory
        state.conversation_memory[0]["question"] = state.question

        return state


request_routing_node = RequestRouterNode(
    model=request_routing_model, prompt=request_routing_prompt
)
