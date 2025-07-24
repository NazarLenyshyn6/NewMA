"""..."""

from abc import ABC, abstractmethod
from typing import Dict, Callable
from pathlib import Path

import pandas as pd
from fastapi import UploadFile, HTTPException, status


class IStorage(ABC):
    """..."""

    _loaders: Dict[str, Callable] = {
        "csv": pd.read_csv,
        "parquet": pd.read_parquet,
        "pkl": pd.read_pickle,
        "pickle": pd.read_pickle,
    }

    @property
    def valid_extensions(self) -> str:
        """..."""
        return ", ".join(f".{ext}" for ext in self._loaders.keys())

    @staticmethod
    def _get_extension(path: str) -> str:
        """..."""
        extension = Path(path).suffix.lstrip(".")
        return extension

    def _validate_extension(self, extention: str) -> None:
        if extention not in self._loaders:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file extention: .{extention}. Allowed: {self.valid_extensions}",
            )

    @property
    @abstractmethod
    def storage_type(self) -> str:
        """..."""
        ...

    @abstractmethod
    def __init__(self, uri_scheme: str, *args, **kwargs):
        """..."""
        ...

    @abstractmethod
    async def upload(self, user_id: int, dataset_name: str, file: UploadFile) -> str:
        """..."""
        ...

    @abstractmethod
    def download(self, uri: str) -> pd.DataFrame:
        """..."""
        ...

    @abstractmethod
    def delete(self, uri: str) -> None:
        """..."""
        ...
