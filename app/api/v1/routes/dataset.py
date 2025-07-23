"""..."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, UploadFile, File, Form


from app.db.manager import db_manager
from app.services.dataset.service import dataset_service
from app.services.auth.service import auth_service


router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.post("/")
async def upload_dataset(
    token: str = Depends(auth_service.oauth2_scheme),
    db: Session = Depends(db_manager.get_db),
    file: UploadFile = File(...),
    name: str = Form(...),
):
    """..."""
    user = auth_service.get_current_user(db=db, token=token)
    return await dataset_service.save_dataset(
        db=db, file=file, name=name, user_id=user.id
    )


@router.get("/")
def get_datasets(
    token: str = Depends(auth_service.oauth2_scheme),
    db: Session = Depends(db_manager.get_db),
):
    """..."""
    user = auth_service.get_current_user(db=db, token=token)
    return dataset_service.get_datasets(db=db, user_id=user.id)


@router.get("/{name}")
def get_dataset(
    name: str,
    token: str = Depends(auth_service.oauth2_scheme),
    db: Session = Depends(db_manager.get_db),
):
    """..."""
    user = auth_service.get_current_user(db=db, token=token)
    return dataset_service.get_dataset(db=db, name=name, user_id=user.id)


@router.delete("/{name}")
def delete_dataset(
    name: str,
    token: str = Depends(auth_service.oauth2_scheme),
    db: Session = Depends(db_manager.get_db),
):
    """..."""
    user = user = auth_service.get_current_user(db=db, token=token)
    dataset_service.delete_dataset(db=db, user_id=user.id, name=name)
