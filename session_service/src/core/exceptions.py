"""..."""


class SessionNotFoundError(Exception):
    """Raised when a session is not found in the database."""

    pass


class ActiveSessionNotFoundError(Exception):
    """Raised when no active session exists for a user."""

    pass


class ActiveSessionDeletionError(Exception):
    """Raised when attempting to delete an active session which is not allowed."""

    pass


class DuplicateSessionTitleError(Exception):
    """Raised when a session with the same title already exists for the user."""

    pass
