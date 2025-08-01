"""..."""


class BaseSubTask(str):
    """..."""

    OTHER = "OTHER"

    @classmethod
    def from_string(cls, subtask_str: str):
        """..."""
        try:
            return cls(subtask_str.strip())
        except ValueError:
            return cls.OTHER
