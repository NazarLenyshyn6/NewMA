"""..."""


class SessionNotFoundError(Exception):
    """Raised when a session is not found in the database."""

    ...


class ActiveSessionNotFoundError(Exception):
    """Raised when no active session exists for a user."""

    ...


class ActiveSessionDeletionError(Exception):
    """Raised when attempting to delete an active session which is not allowed."""

    ...


class DuplicateSessionTitleError(Exception):
    """Raised when a session with the same title already exists for the user."""

    ...
