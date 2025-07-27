"""..."""

from core.enums import StorageType
from schemas.base import BaseSchema


class FileCreate(BaseSchema):
    """..."""

    file_name: str
    storage_uri: str
    description: str
    summary: str
    storage_type: StorageType
    user_id: int


class FileRead(BaseSchema):
    """..."""

    file_name: str
    storage_uri: str
    description: str
    summary: str


class ActiveFile(BaseSchema):
    """..."""

    file_name: str
