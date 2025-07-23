"""..."""

from typing_extensions import override
from pathlib import Path
import shutil


import pandas as pd
from fastapi import UploadFile, HTTPException, status

from app.core.config import settings
from app.repositories.dataset.storage.base import IStorage


class LocalStorage(IStorage):
    """..."""

    def __init__(self, base_path: str, uri_scheme: str):
        self.base_path = Path(base_path)
        self.uri_scheme = uri_scheme
        self.base_path.mkdir(parents=True, exist_ok=True)

    @override
    async def upload(self, user_id: int, dataset_name: str, file: UploadFile) -> str:
        extension = self._get_extension(file.filename)
        self._validate_extension(extension)
        path = self.base_path / f"{user_id}_{dataset_name}.{extension}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return f"{self.uri_scheme}{path}"

    @override
    def download(self, uri: str) -> pd.DataFrame:
        extension = self._get_extension(uri)
        self._validate_extension(extension)
        path = Path(uri.replace(self.uri_scheme, ""))
        if not path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No file found at path: {path}",
            )
        return self._loaders[extension](path)

    @override
    def delete(self, uri: str) -> None:
        path = Path(uri.replace(self.uri_scheme, ""))
        if path.exists():
            path.unlink()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No file found at path: {path}",
            )


local_storage = LocalStorage(
    base_path=settings.local_storage.LOCAL_STORAGE_PATH, uri_scheme="local://"
)
