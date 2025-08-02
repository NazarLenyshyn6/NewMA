"""..."""

from langchain_anthropic import ChatAnthropic

from agent.core.config import settings

anthropic_claude_sonnet_4_20250514_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
)
