"""..."""

from uuid import UUID

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
        url: str = "http://127.0.0.1:8005/api/v1/chat",
    ):
        """..."""
        data = {
            "question": question,
            "user_id": user_id,
            "session_id": session_id,
            "file_name": file_name,
            "storage_uri": storage_uri,
        }
        response = requests.post(url=url, json=data)
        return AgentClient._handle_response(response)
