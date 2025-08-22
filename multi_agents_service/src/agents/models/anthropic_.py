"""..."""

from langchain_anthropic import ChatAnthropic

from core.config import settings

# Expert Mode
expert_suggestion_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.2,  # Tested 0.5
    max_tokens=8000,
    streaming=True,
)

expert_solution_planing_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.25,
    max_tokens=8000,
    stream_usage=True,
)


expert_execution_planing_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.2,
    max_tokens=8000,
    stream_usage=True,
)

expert_reporting_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.3,  # Tested 0.5
    max_tokens=8000,
    streaming=True,
)

# Insight Mode


# Common
code_mode_routing_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,
)

request_routing_model = ChatAnthropic(
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

lambda_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,  # Tested 0.2
    max_tokens=40000,
    top_k=None,
    top_p=1,
)

summarization_model = ChatAnthropic(
    model_name="claude-sonnet-4-20250514",
    anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
    temperature=0.0,  # Tested 0.2
    max_tokens=40000,
    top_k=None,
    top_p=1,
)
