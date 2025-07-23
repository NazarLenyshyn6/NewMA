"""..."""

from dataclasses import dataclass
from typing import List

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd

from app.repositories.dataset.repository import dataset_repository, DatasetRepository
from app.schemas import dataset as dataset_schemas


@dataclass
class DatasetService:
    repository: DatasetRepository

    async def save_dataset(
        self, db: Session, file: UploadFile, name: str, user_id: int
    ) -> None:
        """..."""
        # Upload file to storate
        uri = await self.repository.upload_to_storage(
            user_id=user_id, dataset_name=name, file=file
        )

        # Merge all metadata
        summary = "summarizer..."
        dataset = {
            "name": name,
            "uri": uri,
            "summary": summary,
            "user_id": user_id,
        }

        # Save to DB
        self.repository.create_dataset(db=db, dataset=dataset)

    def download_dataset(self, db: Session, name: str, user_id: int) -> pd.DataFrame:
        """..."""
        db_dataset = self.repository.get_dataset(db=db, name=name, user_id=user_id)
        if db_dataset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataset {name} not found.",
            )
        return self.repository.download_from_storage(uri=db_dataset.uri)

    def delete_dataset(self, db: Session, user_id: int, name: str) -> None:
        """..."""
        db_dataset = self.repository.get_dataset(db=db, user_id=user_id, name=name)
        if not db:
            return
        self.repository.delete_dataset(db=db, user_id=user_id, name=name)
        self.repository.delete_from_storage(uri=db_dataset.uri)

    def get_datasets(
        self, db: Session, user_id: int
    ) -> List[dataset_schemas.DatasetRead]:
        """..."""
        db_datasets = self.repository.get_datasets(db=db, user_id=user_id)
        return [
            dataset_schemas.DatasetRead.model_validate(dataset)
            for dataset in db_datasets
        ]

    def get_dataset(
        self, db: Session, name: str, user_id: int
    ) -> dataset_schemas.DatasetRead:
        """..."""
        db_dataset = self.repository.get_dataset(db=db, name=name, user_id=user_id)
        if db_dataset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataset {name} not found.",
            )
        return dataset_schemas.DatasetRead.model_validate(db_dataset)


dataset_service = DatasetService(repository=dataset_repository)
