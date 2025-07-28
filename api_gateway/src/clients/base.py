"""..."""

import requests


class BaseClient:
    @staticmethod
    def _handle_response(response: requests.Response):
        """..."""
        response.raise_for_status()

        try:
            return response.json()
        except ValueError as e:
            raise requests.HTTPError(
                f"Failed to parse JSON response. Response text: {response.text}",
                response=response,
            ) from e
