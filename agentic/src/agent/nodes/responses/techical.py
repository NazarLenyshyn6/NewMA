"""..."""

from typing import override, Optional, List
from uuid import UUID
import pickle

from sqlalchemy.orm import Session

from agent.nodes.base import BaseNode
from agent.prompts.responses.technical import technical_response_prompt
from agent.models.anthropic_ import techical_response_model
from services.memory import agent_memory_service


class TechicalResponseNode(BaseNode):
    """..."""

    @staticmethod
    def _parse_analysis_report(analysis_report: list) -> str:
        """..."""
        lines = []
        for i, step in enumerate(analysis_report, 1):
            lines.append(f"Step {i}: {step.get('step', '')}")
            lines.append(f"  Purpose: {step.get('why', '')}")
            lines.append(f"  Key Finding: {step.get('finding', '')}")
            lines.append(f"  Actions Taken: {step.get('action', '')}")
            lines.append(f"  Data Summary: {step.get('data_summary', '')}")
            alerts = step.get("alerts")
            if alerts:
                lines.append(f"  Alerts: {alerts}")
            recommendation = step.get("recommendation")
            if recommendation:
                lines.append(f"  Recommendation: {recommendation}")
            lines.append("")  # Blank line for spacing

        return "\n".join(lines)

    @override
    def run(
        self,
        question: str,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
    ): ...

    @override
    async def arun(
        self,
        question: str,
        instruction: str,
        analysis_report: List,
        db: Optional[Session] = None,
        user_id: Optional[int] = None,
        session_id: Optional[UUID] = None,
        file_name: Optional[str] = None,
        storage_uri: Optional[str] = None,
    ):
        """..."""
        self._token_buffer = []
        report = self._parse_analysis_report(analysis_report)
        async for chunk in self._chain.astream(
            {"question": question, "report": report, "instruction": instruction}
        ):
            chunk = chunk.content
            self._token_buffer.append(chunk)
            yield chunk


techical_response_node = TechicalResponseNode(
    model=techical_response_model,
    prompt=technical_response_prompt,
    memory=agent_memory_service,
)
