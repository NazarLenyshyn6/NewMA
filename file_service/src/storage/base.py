"""..."""

from typing import ClassVar, Set
from abc import ABC, abstractmethod
from pathlib import Path

from fastapi import UploadFile

from core.exceptions import UnsupportedFileExtensionError


class BaseStorage(ABC):
    """..."""

    allowed_file_extensions: ClassVar[Set[str]] = {"csv"}

    @staticmethod
    def get_file_extension(path: str) -> str:
        """..."""
        return Path(path).suffix.lstrip(".").lower()

    @classmethod
    def validate_file_extension(cls, file_extension: str) -> None:
        """..."""
        if file_extension not in cls.allowed_file_extensions:
            allowed = ", ".join(sorted(cls.allowed_file_extensions))
            raise UnsupportedFileExtensionError(
                f"Invalid file extension: .{file_extension}. Allowed: {allowed}"
            )

    @classmethod
    @abstractmethod
    def upload_file(cls, user_id: int, file_name: str, file: UploadFile) -> str:
        """..."""
        ...

    @staticmethod
    @abstractmethod
    def delete_file(storage_uri: str) -> None:
        """..."""
        ...
