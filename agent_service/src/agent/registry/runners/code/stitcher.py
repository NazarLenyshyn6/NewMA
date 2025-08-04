"""..."""

from agent.registry.models.anthropic_ import anthropic_code_stitching_model
from agent.runners.code.stitcher import CodeStitchingRunner
from agent.prompts.code.stitcher import code_stitching_prompt


code_stitching_runner = CodeStitchingRunner(
    model=anthropic_code_stitching_model, prompt=code_stitching_prompt
)
