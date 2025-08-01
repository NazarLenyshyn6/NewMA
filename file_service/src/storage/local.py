"""..."""

from typing_extensions import override
from pathlib import Path
import shutil

from fastapi import UploadFile

from core.config import settings
from storage.base import BaseStorage


class LocalStorage(BaseStorage):
    """..."""

    base_path: Path = Path(settings.local_storage.LOCAL_STORAGE_PATH)

    @classmethod
    def _initialize_storage(cls) -> None:
        """..."""
        if not cls.base_path.exists():
            cls.base_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    @override
    def upload_file(cls, user_id: int, file_name: str, file: UploadFile) -> str:
        cls._initialize_storage()
        file_extension = cls.get_file_extension(file.filename)
        cls.validate_file_extension(file_extension)
        path = cls.base_path / f"{user_id}_{file_name}.{file_extension}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return f"local://{path}"

    @staticmethod
    @override
    def delete_file(storage_uri: str) -> None:
        path = Path(storage_uri.replace("local://", ""))
        if path.exists():
            path.unlink()
