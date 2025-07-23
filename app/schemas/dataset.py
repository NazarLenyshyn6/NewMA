"""..."""

from app.schemas.base import BaseSchema


class DatasetRead(BaseSchema):
    """..."""

    name: str
    uri: str
    summary: str
