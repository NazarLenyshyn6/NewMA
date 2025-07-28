"""..."""

import requests

from clients.base import BaseClient


class AuthClient(BaseClient):
    """..."""

    @staticmethod
    def register_user(
        email: str,
        password: str,
        url: str = "http://127.0.0.1:8000/api/v1/auth/register",
    ):
        """..."""
        user_data = {"email": email, "password": password}
        response = requests.post(url=url, json=user_data)
        return AuthClient._handle_response(response)

    @staticmethod
    def login(
        email: str, password: str, url: str = "http://127.0.0.1:8000/api/v1/auth/login"
    ):
        """..."""
        data = {
            "username": email,  # OAuth2 expects "username" field
            "password": password,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url=url, data=data, headers=headers)
        return AuthClient._handle_response(response)

    @staticmethod
    def get_current_user(token: str, url: str = "http://127.0.0.1:8000/api/v1/auth/me"):
        """..."""
        headers = {
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url=url, headers=headers)
        return AuthClient._handle_response(response)
