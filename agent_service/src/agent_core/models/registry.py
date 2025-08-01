"""..."""

from agent_core.models.anthropic import build_anthropic_model
from agent_core.core.config import settings


anthropic_claude_sonnet_4_20250514_model = build_anthropic_model(
    model_name="claude-sonnet-4-20250514",
    api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
)
