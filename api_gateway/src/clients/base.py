"""..."""

import requests

from core.exceptions import ClientError


class BaseClient:
    @staticmethod
    def _handle_response(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ClientError(
                status_code=response.status_code,
                message=str(e),
                response_text=response.text,
            )
        try:
            return response.json()
        except ValueError:
            raise ClientError(
                status_code=response.status_code,
                message="Response content is not valid JSON.",
                response_text=response.text,
            )
