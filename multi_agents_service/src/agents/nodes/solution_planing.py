"""..."""

from agents.nodes.base import BaseNode
from agents.prompts.solution_planing.expert import expert_solution_planning_prompt
from agents.models.anthropic_ import expert_solution_planing_model
from agents.schemas.solution_planing import SolutionPlanningOutput
from agents.state import AgentState


class SolutionPlaningNode(BaseNode):

    def plan(self, state: AgentState) -> AgentState:
        print("* SolutionPlaningNode -> ")
        state.subtasks = self._chain.invoke(
            {
                "question": state.question,
                "conversation_summary_memory": state.conversation_summary_memory,
            },
            config={"metadata": {"stream": False}},
        ).subtasks
        return state


expert_solution_planing_node = SolutionPlaningNode(
    model=expert_solution_planing_model,
    prompt=expert_solution_planning_prompt,
    output_schema=SolutionPlanningOutput,
)
