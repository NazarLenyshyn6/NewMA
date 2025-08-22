"""..."""

from agents.nodes.base import BaseNode
from agents.prompts.code.debagging.expert import (
    expert_code_debugging_prompt,
)
from agents.models.anthropic_ import code_generation_model
from agents.state import AgentState


class CodeDebaggingNode(BaseNode):
    """..."""

    def debug(self, state: AgentState) -> AgentState:
        print("* CodeDebaggingNode -> ")
        state.code = self._chain.invoke(
            {
                "dependencies": state.dependencies,
                "dataset_summary": state.dataset_summary,
                "code_summary_memory": state.code_summary_memory,
                "variables_memory": state.variables_memory.keys(),
                "code": state.code,
                "error_message": state.code_error,
                "question": state.question,
            },
            config={"metadata": {"checkpoint": "Debagging..."}},
        ).content
        state.current_code_debagging_attempt = state.current_code_debagging_attempt + 1

        # Add debaggign code to conversation memory
        state.conversation_memory[0]["answer"] = (
            state.conversation_memory[0]["answer"] + state.code
        )
        return state


expert_code_debagging_node = CodeDebaggingNode(
    model=code_generation_model, prompt=expert_code_debugging_prompt
)
