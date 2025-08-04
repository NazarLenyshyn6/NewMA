"""..."""

import httpx
from uuid import UUID
from typing import AsyncGenerator

import requests

from clients.base import BaseClient


class AgentClient(BaseClient):
    """..."""

    @staticmethod
    def chat(
        question: str,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        dataset_summary: str,
        url: str = "http://127.0.0.1:8005/api/v1/chat",
    ):
        """..."""
        data = {
            "question": question,
            "user_id": user_id,
            "session_id": session_id,
            "file_name": file_name,
            "storage_uri": storage_uri,
            "dataset_summary": dataset_summary,
        }
        response = requests.post(url=url, json=data)
        return AgentClient._handle_response(response)

    @staticmethod
    async def chat_stream(
        question: str,
        user_id: int,
        session_id: UUID,
        file_name: str,
        storage_uri: str,
        dataset_summary: str,
        url: str = "http://127.0.0.1:8005/api/v1/chat/stream",
    ) -> AsyncGenerator[str, None]:
        """Stream chat response from agent service."""
        payload = {
            "question": question,
            "user_id": user_id,
            "session_id": str(session_id),
            "file_name": file_name,
            "storage_uri": storage_uri,
            "dataset_summary": dataset_summary,
        }

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(chunk_size=1):
                    if chunk:
                        yield chunk
