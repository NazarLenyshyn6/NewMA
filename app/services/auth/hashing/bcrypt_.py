"""..."""

from typing_extensions import override

from passlib.context import CryptContext

from app.services.auth.hashing import base as hashing_base


class BcryptHasher(hashing_base.IHasher):
    """..."""

    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @override
    def hash(self, password: str) -> str:
        return self._context.hash(password)

    @override
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._context.verify(plain_password, hashed_password)


bcrypt_hasher = BcryptHasher()
