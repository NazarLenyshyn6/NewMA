"""..."""

from agent.registry.models.anthropic_ import anthropic_claude_sonnet_4_20250514_model
from agent.prompts.classifiers.flow import flow_classification_prompt
from agent.classifiers.flow import FlowClassifier

flow_classifier = FlowClassifier(
    model=anthropic_claude_sonnet_4_20250514_model, prompt=flow_classification_prompt
)
