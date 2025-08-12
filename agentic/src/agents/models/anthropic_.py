"""..."""

from langchain_anthropic import ChatAnthropic

from core.config import settings


# Techical Mode
routing_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,
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


planning_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.2,  # Tested 0.3
    max_tokens=8000,
    stream_usage=True,
)


techical_response_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.3,  # Tested 0.5
    max_tokens=8000,
    streaming=True,
)

techical_conversation_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.2,  # Tested 0.5
    max_tokens=8000,
    streaming=True,
)

# Business Mode


# Common
summarization_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,  # Tested 0.2
    max_tokens=40000,
    top_k=None,
    top_p=1,
)

business_conversation_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.6,  # Tested 0.5
    max_tokens=8000,
    streaming=True,
)
