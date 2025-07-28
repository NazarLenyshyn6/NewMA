"""..."""

from uuid import UUID
from typing import Optional

import requests
from fastapi import UploadFile, HTTPException, status

from clients.base import BaseClient


class FileClient(BaseClient):
    """..."""

    @staticmethod
    def get_files(token: str, url: str = "http://127.0.0.1:8002/api/v1/files"):
        """..."""
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url=url, headers=headers)
        return FileClient._handle_response(response)

    @staticmethod
    def get_active_file(
        token: str,
        session: UUID,
        base_url: str = "http://127.0.0.1:8002/api/v1/files/active",
    ):
        """..."""
        url = base_url + f"/{session}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url=url, headers=headers)
        return FileClient._handle_response(response)

    @staticmethod
    def set_active_file(
        token: str,
        session: UUID,
        file_name: str,
        base_url: str = "http://127.0.0.1:8002/api/v1/files/active",
    ):
        """..."""
        url = base_url + f"/{session}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        data = {"file_name": file_name}
        response = requests.post(url=url, headers=headers, json=data)
        return FileClient._handle_response(response)

    @staticmethod
    def upload_file(
        token: str,
        file_name: str,
        session_id: UUID,
        description: str,
        file: UploadFile,
        url="http://127.0.0.1:8002/api/v1/files",
    ):
        """..."""
        files = {"file": (file.filename, file.file, file.content_type)}

        data = {
            "file_name": file_name,
            "session_id": session_id,
            "description": description,
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.post(url=url, files=files, data=data, headers=headers)
        return FileClient._handle_response(response)

    @staticmethod
    def delete_file(
        token: str,
        file_name: str,
        active_file_name: Optional[str],
        base_url: str = "http://127.0.0.1:8002/api/v1/files",
    ):
        """..."""
        if file_name == active_file_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delite active file; please deactivate it first",
            )
        url = base_url + f"/{file_name}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.delete(url=url, headers=headers)
        return FileClient._handle_response(response)
