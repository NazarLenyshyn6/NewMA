"""..."""

import requests

from clients.base import BaseClient


class SessionClient(BaseClient):
    """..."""

    @staticmethod
    def get_sessions(token: str, url: str = "http://127.0.0.1:8001/api/v1/sessions"):
        """..."""
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url=url, headers=headers)
        return SessionClient._handle_response(response)

    @staticmethod
    def get_active_session_id(
        token: str, url: str = "http://127.0.0.1:8001/api/v1/sessions/active"
    ):
        """..."""
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url=url, headers=headers)
        return SessionClient._handle_response(response)

    @staticmethod
    def create_session(
        token: str, title: str, url="http://127.0.0.1:8001/api/v1/sessions"
    ):
        """..."""
        headers = {
            "Authorization": f"Bearer {token}",
        }
        data = {"title": title}
        response = requests.post(url=url, json=data, headers=headers)
        return SessionClient._handle_response(response)

    @staticmethod
    def set_active_session(
        token: str,
        title: str,
        base_url: str = "http://127.0.0.1:8001/api/v1/sessions/active",
    ):
        """..."""
        url = base_url + f"/{title}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.post(url=url, headers=headers)
        return SessionClient._handle_response(response)

    @staticmethod
    def delete_session(
        token: str, title: str, base_url: str = "http://127.0.0.1:8001/api/v1/sessions"
    ):
        url = base_url + f"/{title}"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.delete(url=url, headers=headers)
        return SessionClient._handle_response(response)
