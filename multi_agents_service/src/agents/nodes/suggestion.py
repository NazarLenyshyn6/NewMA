"""..."""

from agents.nodes.base import BaseNode
from agents.prompts.suggestion.expert import expert_suggestion_prompt
from agents.models.anthropic_ import expert_suggestion_model
from agents.state import AgentState
from agents.nodes.summarization import SummarizationNode


class SuggestionNode(BaseNode):

    def suggest(self, state: AgentState):
        """..."""
        print("* SuggestionNode -> ")
        state.suggestion = self._chain.invoke(
            {"question": state.question, "history": state.conversation_summary_memory}
        ).content

        state.conversation_summary_memory = (
            SummarizationNode.conversation_summarization(
                conversation_summary_memory=state.conversation_summary_memory,
                report=state.suggestion,
            )
        )

        # Add to conversation memory
        state.conversation_memory[0]["answer"] = (
            state.conversation_memory[0]["answer"] + state.suggestion
        )
        return state


expert_suggestion_node = SuggestionNode(
    model=expert_suggestion_model, prompt=expert_suggestion_prompt
)
