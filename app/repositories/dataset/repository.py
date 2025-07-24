"""..."""

from dataclasses import dataclass
from typing import Optional, List

import pandas as pd
from sqlalchemy.orm import Session
from fastapi import UploadFile


from app.core.logger_setup import configure_logger
from app.models.dataset import Dataset
from app.repositories.dataset.storage.base import IStorage
from app.repositories.dataset.storage.local import local_storage


logger = configure_logger(
    name="repository_dataset", subfolder="repositories", filename="dataset.log"
)


@dataclass
class DatasetRepository:
    """..."""

    storage: IStorage

    async def upload_to_storage(
        self, user_id: int, dataset_name: str, file: UploadFile
    ) -> str:
        """..."""
        logger.info(
            "Uploading dataset '%s' for user_id=%s to %s storage",
            dataset_name,
            user_id,
            self.storage.storage_type,
        )
        try:
            uri = await self.storage.upload(
                user_id=user_id, dataset_name=dataset_name, file=file
            )
            return uri
        except Exception:
            logger.exception(
                "Failed to upload dataset '%s' to user_id=%s to %s storage",
                dataset_name,
                user_id,
                self.storage.storage_type,
            )
            raise

    def download_from_storage(self, uri: str) -> pd.DataFrame:
        """..."""
        logger.info("Downloading dataset from uri=%s", uri)
        try:
            df = self.storage.download(uri=uri)
            return df
        except Exception:
            logger.exception("Failed to download dataset from uri=%s", uri)
            raise

    def delete_from_storage(self, uri: str) -> None:
        """..."""
        logger.info("Deleting dataset from uri=%s", uri)
        try:
            self.storage.delete(uri=uri)
        except Exception:
            logger.exception("Failed to delete dataset from uri=%s", uri)
            raise

    @staticmethod
    def get_datasets(db: Session, user_id: int) -> List[Dataset]:
        """..."""
        logger.debug("Fetching all datasets for user_id=%s", user_id)
        datasets = db.query(Dataset).where(Dataset.user_id == user_id).all()
        logger.debug("Found %s datasets for user_id=%s", user_id)
        return datasets

    @staticmethod
    def get_dataset(db: Session, name: str, user_id: int) -> Optional[Dataset]:
        """..."""
        logger.debug("Fetchind dataset '%s' for user_id=%s", name, user_id)
        dataset = (
            db.query(Dataset)
            .where((Dataset.name == name) & (Dataset.user_id == user_id))
            .first()
        )
        if dataset is None:
            logger.warning("Dataset '%s' not found for user_id=%s", name, user_id)
        return dataset

    @staticmethod
    def create_dataset(db: Session, dataset: dict) -> Dataset:
        """..."""
        logger.info(
            "Creating dataset '%s' for user_id=%s",
            dataset.get("name"),
            dataset.get("user_id"),
        )
        db_dataset = Dataset(**dataset)
        try:
            db.add(db_dataset)
            db.commit()
            db.refresh(db_dataset)
            return db_dataset
        except Exception:
            db.rollback()
            logger.exception(
                "Failed to create '%s' for user_id=%s",
                dataset.get("name"),
                dataset.get("user_id"),
            )
            raise

    @classmethod
    def delete_dataset(cls, db: Session, user_id: int, name: str) -> None:
        """..."""
        logger.info("Deleting dataset '%s' for user_id=%s", name, user_id)
        db_dataset = cls.get_dataset(db=db, name=name, user_id=user_id)
        if db_dataset is None:
            logger.warning(
                "Dataset '%s' not found for deletion for user_id=%s", name, user_id
            )
            return
        try:
            db.delete(db_dataset)
            db.commit()
        except Exception:
            db.rollback()
            logger.exception(
                "Failed to delete dataset %s for user_id=%s", name, user_id
            )
            raise


dataset_repository = DatasetRepository(storage=local_storage)
