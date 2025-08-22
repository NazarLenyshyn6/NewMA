"""..."""

from uuid import UUID
import json

from sqlalchemy.orm import Session

from agents.graphs.builder import expert_agent


class AgentService:

    @staticmethod
    async def expert_agent_stream(
        question: str,
        db: Session,
        user_id: int,
        file_name: str,
        session_id: UUID,
        storage_uri: str,
        dataset_summary: str,
    ):
        """..."""
        async for chunk in expert_agent.astream_events(
            {
                "question": question,
                "db": db,
                "user_id": user_id,
                "file_name": file_name,
                "session_id": session_id,
                "storage_uri": storage_uri,
                "dataset_summary": dataset_summary,
            },
        ):
            # Steam image
            if (
                chunk["metadata"].get("image", False)
                and chunk["event"] == "on_chain_end"
                and chunk["data"].get("output", False)
            ):
                data = chunk["data"]["output"].content
                yield f"data: {json.dumps({'type': 'image', 'data': data})}\n\n"

            # Stream text
            if chunk["event"] == "on_chat_model_stream":
                stream = chunk["metadata"].get("stream", True)
                if stream:
                    data = chunk["data"]["chunk"].content
                    yield f"data: {json.dumps({'type': 'text', 'data': data})}\n\n"
