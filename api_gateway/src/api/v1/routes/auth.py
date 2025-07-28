"""..."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schemas.auth import RegisterRequest
from clients.auth import AuthClient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/gateway/auth/login")

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme)):
    """..."""
    return AuthClient.get_current_user(token=token)


@router.post("/register")
def register_user(register_request: RegisterRequest):
    return AuthClient.register_user(
        email=register_request.email, password=register_request.password
    )


@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
):
    return AuthClient.login(email=user.username, password=user.password)
