"""..."""

from pydantic import BaseModel


class ActiveFileRequest(BaseModel):
    """..."""

    file_name: str
