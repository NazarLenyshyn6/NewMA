"""..."""

import pickle
from agents.nodes.base import BaseNode
from agents.prompts.code.generation.code_gen.expert import (
    expert_code_gen_prompt,
)
from agents.models.anthropic_ import code_generation_model
from agents.state import AgentState
from services.memory.code_summary import code_summary_memory_service
from services.memory.variables import variables_memory_service


class CodeGenNode(BaseNode):
    """..."""

    def generate(self, state: AgentState) -> AgentState:
        """..."""
        print("* CodeGenNode -> ")
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
                "dependencies": state.dependencies,
                "dataset_summary": state.dataset_summary,
                "code_summary_memory": state.code_summary_memory,
                "variables_memory": state.variables_memory.keys(),
                "execution_plan": state.execution_plan,
            },
            config={"metadata": {"checkpoint": "Generating code ..."}},
        ).content

        # Add generated code to conversation memory
        state.conversation_memory[0]["answer"] = (
            state.conversation_memory[0]["answer"] + state.code
        )
        return state


expert_code_gen_node = CodeGenNode(
    model=code_generation_model, prompt=expert_code_gen_prompt
)
