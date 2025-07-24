"""..."""

from typing_extensions import override
from pathlib import Path
import shutil


import pandas as pd
from fastapi import UploadFile, HTTPException, status

from app.core.config import settings
from app.core.logger_setup import configure_logger
from app.repositories.dataset.storage.base import IStorage

logger = configure_logger(
    name="storage_local", subfolder="storages", filename="local.log"
)


class LocalStorage(IStorage):
    """..."""

    def __init__(self, base_path: str, uri_scheme: str):
        self.base_path = Path(base_path)
        self.uri_scheme = uri_scheme
        self.base_path.mkdir(parents=True, exist_ok=True)

    @property
    @override
    def storage_type(self) -> str:
        return "local"

    @override
    async def upload(self, user_id: int, dataset_name: str, file: UploadFile) -> str:
        logger.info(
            "Uploading file for user_id=%s, dataset_name=%s, filename=%s",
            user_id,
            dataset_name,
            file.filename,
        )
        extension = self._get_extension(file.filename)
        self._validate_extension(extension)
        path = self.base_path / f"{user_id}_{dataset_name}.{extension}"
        try:
            with open(path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info("File uploaded successfully to %s", path)
        except Exception:
            logger.exception("Failed to upload file to path: %s", path)
            raise
        return f"{self.uri_scheme}{path}"

    @override
    def download(self, uri: str) -> pd.DataFrame:
        logger.info("Downloading file from uri=%s", uri)
        extension = self._get_extension(uri)
        self._validate_extension(extension)
        path = Path(uri.replace(self.uri_scheme, ""))
        if not path.exists():
            logger.error("File not found at path: %s", path)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found at path: {path}",
            )
        return self._loaders[extension](path)

    @override
    def delete(self, uri: str) -> None:
        logger.info("Deleting file at uri=%s", uri)
        path = Path(uri.replace(self.uri_scheme, ""))
        if path.exists():
            path.unlink()
            logger.info("File deleted at uri=%s", uri)
        else:
            logger.info("Attempting to delete non-existing file at path: %s", path)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File not found at path: {path}",
            )


local_storage = LocalStorage(
    base_path=settings.local_storage.LOCAL_STORAGE_PATH, uri_scheme="local://"
)
