"""..."""

import pickle
from agents.nodes.base import BaseNode
from agents.prompts.code.generation.visualization_gen.expert import (
    expert_visualization_gen_prompt,
)
from agents.models.anthropic_ import code_generation_model
from agents.state import AgentState
from services.memory.code_summary import code_summary_memory_service
from services.memory.variables import variables_memory_service


class VisualizationGenNode(BaseNode):
    """..."""

    def generate(self, state: AgentState) -> AgentState:
        """..."""
        print("* VisualizationGenNode -> ")

        # Retvier all requied information from memory and store in graph
        if state.code_summary_memory is None:
            state.code_summary_memory = pickle.loads(
                code_summary_memory_service.get_memory(
                    db=state.db,
                    user_id=state.user_id,
                    session_id=state.session_id,
                    file_name=state.file_name,
                    storage_uri=state.storage_uri,
                ).memory
            )
        if state.variables_memory is None:
            state.variables_memory = pickle.loads(
                variables_memory_service.get_memory(
                    db=state.db,
                    user_id=state.user_id,
                    session_id=state.session_id,
                    file_name=state.file_name,
                    storage_uri=state.storage_uri,
                ).memory
            )
        state.code = self._chain.invoke(
            {
                "dataset_summary": state.dataset_summary,
                "code_summary_memory": state.code_summary_memory,
                "variables_memory": state.variables_memory.keys(),
                "execution_plan": state.execution_plan,
            },
        ).content

        # Add generated code to conversation memory
        state.conversation_memory[0]["answer"] = (
            state.conversation_memory[0]["answer"] + state.code
        )
        return state


expert_visualization_gen_node = VisualizationGenNode(
    model=code_generation_model, prompt=expert_visualization_gen_prompt
)
