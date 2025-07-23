"""..."""

from dataclasses import dataclass
from typing import Optional, List

import pandas as pd
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories.dataset.storage.base import IStorage
from app.repositories.dataset.storage.local import local_storage
from app.models import dataset as dataset_models


@dataclass
class DatasetRepository:
    """..."""

    storage: IStorage

    async def upload_to_storage(
        self, user_id: int, dataset_name: str, file: UploadFile
    ) -> str:
        """..."""
        return await self.storage.upload(
            user_id=user_id, dataset_name=dataset_name, file=file
        )

    def download_from_storage(self, uri: str) -> pd.DataFrame:
        """..."""
        return self.storage.download(uri=uri)

    def delete_from_storage(self, uri: str) -> None:
        """..."""
        return self.storage.delete(uri=uri)

    @staticmethod
    def get_datasets(db: Session, user_id: int) -> List[dataset_models.Dataset]:
        """..."""
        return (
            db.query(dataset_models.Dataset)
            .where(dataset_models.Dataset.user_id == user_id)
            .all()
        )

    @staticmethod
    def get_dataset(
        db: Session, name: str, user_id: int
    ) -> Optional[dataset_models.Dataset]:
        """..."""
        return (
            db.query(dataset_models.Dataset)
            .where(
                (dataset_models.Dataset.name == name)
                & (dataset_models.Dataset.user_id == user_id)
            )
            .first()
        )

    @staticmethod
    def create_dataset(db: Session, dataset: dict) -> dataset_models.Dataset:
        """..."""
        db_dataset = dataset_models.Dataset(**dataset)
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        return db_dataset

    @classmethod
    def delete_dataset(cls, db: Session, user_id: int, name: str) -> None:
        """..."""
        db_dataset = cls.get_dataset(db=db, name=name, user_id=user_id)
        if db_dataset is None:
            return
        db.delete(db_dataset)
        db.commit()


dataset_repository = DatasetRepository(storage=local_storage)
