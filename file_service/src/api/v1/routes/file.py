"""..."""

from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Form, UploadFile, File

from core.db import db_manager
from core.security import get_current_user_id
from core.enums import StorageType
from schemas.file import FileRead, ActiveFile
from services.file import file_service

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/")
def get_files(
    db: Session = Depends(db_manager.get_db),
    user_id: int = Depends(get_current_user_id),
) -> List[FileRead]:
    return file_service.get_files(db=db, user_id=user_id)


@router.get("/active/{session}")
def get_active_file(
    session: UUID,
    db: Session = Depends(db_manager.get_db),
    user_id: int = Depends(get_current_user_id),
) -> FileRead:
    return file_service.get_active_file(db=db, user_id=user_id, session_id=session)


@router.post("/active/{session}")
def set_active_file(
    active_file: ActiveFile,
    session: UUID,
    db: Session = Depends(db_manager.get_db),
    user_id: int = Depends(get_current_user_id),
):
    file_service.set_active_file(
        db=db, user_id=user_id, session_id=session, file_name=active_file.file_name
    )


@router.post("/")
def upload_file(
    file_name: str = Form(),
    session_id: UUID = Form(),
    description: str = Form(),
    file: UploadFile = File(...),
    db: Session = Depends(db_manager.get_db),
    user_id: int = Depends(get_current_user_id),
) -> FileRead:
    return file_service.upload_file(
        db=db,
        file_name=file_name,
        storage_type=StorageType.LOCAL,
        user_id=user_id,
        session_id=session_id,
        file=file,
        description=description,
    )


@router.delete("/{file_name}")
def delete_file(
    file_name: str,
    db: Session = Depends(db_manager.get_db),
    user_id: int = Depends(get_current_user_id),
):
    return file_service.delete_file(db=db, user_id=user_id, file_name=file_name)
