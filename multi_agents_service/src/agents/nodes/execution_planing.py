"""..."""

from agents.nodes.base import BaseNode
from agents.prompts.execution_planing.expert import expert_execution_planning_prompt
from agents.models.anthropic_ import expert_execution_planing_model
from agents.state import AgentState


class ExecutionPlaningNode(BaseNode):

    def plan(self, state: AgentState) -> AgentState:
        print("* ExecutionPlaningNode -> ")
        state.execution_plan = self._chain.invoke(
            {
                "question": state.subtasks[0],
                "conversation_summary_memory": state.conversation_summary_memory,
            }
        ).content

        # Every new execution plan must be added to conversation history
        state.conversation_memory[0]["answer"] = (
            state.conversation_memory[0]["answer"] + state.execution_plan
        )

        # Null prevous image to avoid showint the same image twice
        state.image = None
        return state


expert_execution_planing_node = ExecutionPlaningNode(
    model=expert_execution_planing_model, prompt=expert_execution_planning_prompt
)
