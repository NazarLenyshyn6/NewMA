"""..."""

from abc import ABC, abstractmethod


class IPasswordHaher(ABC):
    """..."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """..."""
        ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """..."""
        ...
