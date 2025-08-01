"""..."""

from langchain_anthropic import ChatAnthropic


def build_anthropic_model(
    model_name: str, api_key: str, **model_kwargs
) -> ChatAnthropic:
    """..."""
    return ChatAnthropic(
        model_name=model_name, api_key=api_key, model_kwargs=model_kwargs
    )
