"""..."""

from typing import override, Optional, List
from uuid import UUID
import json
from pprint import pformat

from sqlalchemy.orm import Session

from agents.nodes.base import BaseNode
from agents.prompts.technical.reporting import technical_reporting_prompt
from agents.models.anthropic_ import techical_response_model
from services.memory import agent_memory_service


class TechicalResponseNode(BaseNode):
    """..."""

    @staticmethod
    def _parse_analysis_report(analysis_report: list) -> str:
        """..."""

        lines = []
        for i, entry in enumerate(analysis_report, 1):
            lines.append(f"Step {i}:")
            if isinstance(entry, dict):
                for key, value in entry.items():
                    # Use pformat for pretty-printing nested dicts/lists
                    formatted_value = pformat(value, indent=4, width=80)
                    lines.append(f"  {key}: {formatted_value}")
            else:
                # If entry is not a dict, just stringify it
                lines.append(f"  {entry}")
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
        print(report)
        async for chunk in self._chain.astream(
            {"question": question, "report": report, "instruction": instruction}
        ):
            chunk = chunk.content
            self._token_buffer.append(chunk)
            chunk = f"data: {json.dumps({'type': 'text', 'data': chunk})}\n\n"
            yield chunk


techical_reporting_node = TechicalResponseNode(
    model=techical_response_model,
    prompt=technical_reporting_prompt,
    memory=agent_memory_service,
)
