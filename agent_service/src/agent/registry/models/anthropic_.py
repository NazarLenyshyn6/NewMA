"""..."""

from langchain_anthropic import ChatAnthropic

from agent.core.config import settings

anthropic_claude_sonnet_4_20250514_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,
)


anthropic_code_generation_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,
    max_tokens=4096,
    top_k=None,
    top_p=1,
    stop_sequences=["\n\nHuman:", "\n\nSystem:"],
)


anthropic_code_stitching_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,
    max_tokens=50000,
    top_k=None,
    top_p=1,
    streaming=True,
)

anthropic_summary_reporting_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.4,
    max_tokens=4000,
    top_k=None,
    top_p=1,
    streaming=True,
)
