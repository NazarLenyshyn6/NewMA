"""..."""

from dataclasses import dataclass
from typing import Optional
from datetime import timedelta, datetime


from jose import JWTError, jwt
from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.auth.token import TokenData


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
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """..."""
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_access_token(self, token: str, key: str = "sub") -> TokenData:
        """..."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            id = payload.get(key)
            if id is None:
                raise self.credential_exception
            return TokenData(id=id)
        except JWTError as e:
            print(e)
            raise self.credential_exception


jwt_handler = JWTHandler(
    secret_key=settings.jwt.SECRET_KEY,
    algorithm=settings.jwt.ALGORITHM,
    access_token_expire_minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES_TIMEDELTA,
)
