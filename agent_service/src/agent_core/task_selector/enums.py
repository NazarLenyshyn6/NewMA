"""..."""

from enum import Enum


class Task(str, Enum):
    """..."""

    EDA = "EDA"
    CLASSIFICATION = "CLASSIFICATION"
    OTHER = "OTHER"

    @classmethod
    def from_string(cls, task_str: str) -> "Task":
        """..."""
        try:
            return cls(task_str.strip())
        except ValueError:
            return cls.OTHER
