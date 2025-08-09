"""..."""

from langchain_anthropic import ChatAnthropic

from core.config import settings

direct_response_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.7,
    max_tokens=8000,
    streaming=True,
)

contextual_response_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.7,
    max_tokens=8000,
    streaming=True,
)

techical_response_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.5,
    max_tokens=8000,
    streaming=True,
)


desicion_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,
)

planning_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.3,
    stream_usage=True,
)

code_generation_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,
    max_tokens=50000,
    top_k=None,
    top_p=1,
    streaming=True,
)
