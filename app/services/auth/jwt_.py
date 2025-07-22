"""..."""

from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status


@dataclass
class JWTHandler:
    """..."""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: timedelta

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """..."""
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_access_token(self, token: str) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return username
        except JWTError:
            raise credentials_exception
