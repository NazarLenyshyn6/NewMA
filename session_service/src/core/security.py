"""..."""

from dataclasses import dataclass
from datetime import timedelta

from jose import JWTError, jwt
from fastapi import HTTPException, status

from core.config import settings
from schemas.token import TokenData


@dataclass
class JWTHandler:
    """..."""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: timedelta

    @property
    def credential_exception(self) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def decode_access_token(self, token: str, key: str = "sub") -> TokenData:
        """..."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get(key)
            if user_id is None:
                raise self.credential_exception
            return TokenData(user_id=user_id)
        except JWTError:
            raise self.credential_exception


jwt_handler = JWTHandler(
    secret_key=settings.security.SECRET_KEY,
    algorithm=settings.security.ALGORITHM,
    access_token_expire_minutes=settings.security.ACCESS_TOKEN_EXPIRE_MINUTES_TIMEDELTA,
)
