"""..."""

from dataclasses import dataclass
from datetime import timedelta

from jose import JWTError, jwt
from fastapi import HTTPException, status, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import settings


security = HTTPBearer()


@dataclass
class JWTHandler:
    """..."""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: timedelta

    def decode_access_token(self, token: str, key: str = "sub") -> int:
        """..."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get(key)
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: user_id missing",
                )
            return int(user_id)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )


jwt_handler = JWTHandler(
    secret_key=settings.security.SECRET_KEY,
    algorithm=settings.security.ALGORITHM,
    access_token_expire_minutes=settings.security.ACCESS_TOKEN_EXPIRE_MINUTES_TIMEDELTA,
)


def get_current_user_id(token: str) -> int:
    return jwt_handler.decode_access_token(token=token)
