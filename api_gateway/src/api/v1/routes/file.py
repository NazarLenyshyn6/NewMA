"""..."""

from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer

from schemas.file import ActiveFile
from clients.file import FileClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/gateway/auth/login")

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/")
def get_files(token: str = Depends(oauth2_scheme)):
    return FileClient.get_files(token=token)


@router.get("/{session}")
def get_active_file(session: UUID, token: str = Depends(oauth2_scheme)):
    return FileClient.get_active_file(token=token, session=session)


@router.post("/active/{session}")
def set_active_file(
    active_file: ActiveFile, session: UUID, token: str = Depends(oauth2_scheme)
):
    return FileClient.set_active_file(
        token=token, session=session, file_name=active_file.file_name
    )


@router.post("/")
def upload_file(
    file_name: str = Form(),
    session_id: UUID = Form(),
    description: str = Form(),
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
):
    return FileClient.upload_file(
        token=token,
        file=file,
        file_name=file_name,
        session_id=session_id,
        description=description,
    )


@router.delete("/{file_name}")
def delete_file(file_name: str, token: str = Depends(oauth2_scheme)):
    return FileClient.delete_file(token=token, file_name=file_name)
