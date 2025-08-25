"""
Anthropic model factory module.

This module provides a factory function to create preconfigured
Anthropic `ChatAnthropic` models with sensible defaults. It also defines
a set of shared and specialized model instances for common use cases
such as routing, reasoning, summarization, and code generation.

Responsibilities:
    - Centralize Anthropic model creation with consistent configuration.
    - Provide reusable low-, medium-, and high-temperature models.
    - Expose special-purpose models optimized for summarization and code generation.
"""

from typing import Optional

from langchain_anthropic import ChatAnthropic

from core.config import settings


def create_anthropic_model(
    *,
    temperature: float,
    max_tokens: int = 8000,
    streaming: Optional[bool] = False,
    stream_usage: Optional[bool] = False,
    top_k: Optional[int] = None,
    top_p: Optional[float] = None,
) -> ChatAnthropic:
    """
    Factory for Anthropic chat models with sensible defaults.
    """
    return ChatAnthropic(
        model_name="claude-sonnet-4-20250514",
        anthropic_api_key=settings.anthropic_model.ANTHROPIC_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
        streaming=streaming,
        stream_usage=stream_usage,
        top_k=top_k,
        top_p=top_p,
    )


# --- General-purpose shared models ---
low_temp_model = create_anthropic_model(
    temperature=0.0,  # deterministic / routing / summarization
)

medium_temp_model = create_anthropic_model(
    temperature=0.2,  # balanced reasoning
)

high_temp_model = create_anthropic_model(
    temperature=0.3,  # more creative / explorative
)


# --- Special-purpose overrides ---
code_generation_model = create_anthropic_model(
    temperature=0.0,
    max_tokens=50000,
    streaming=True,
    top_p=1,
)

summarization_model = create_anthropic_model(
    temperature=0.0,
    max_tokens=40000,
    top_p=1,
)
