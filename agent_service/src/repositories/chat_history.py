"""..."""

from uuid import UUID
from typing import Optional

from sqlalchemy.orm import Session

from core.exceptions import ChatHistoryNotFound
from schemas.chat_history import ChatHistory as ChatHistorySchema
from models.chat_history import ChatHistory as ChatHistoryModel


class ChatHistoryRepository:
    """..."""

    @classmethod
    def create_chat_history(
        cls, db: Session, chat_history: ChatHistorySchema
    ) -> ChatHistoryModel:
        """..."""
        db_chat_history = ChatHistoryModel(**chat_history.model_dump())
        db.add(db_chat_history)
        db.commit()
        db.refresh(db_chat_history)
        return db_chat_history

    @classmethod
    def get_chat_history(
        cls, db: Session, user_id: int, session_id: UUID, file_name: str
    ) -> Optional[ChatHistoryModel]:
        return (
            db.query(ChatHistoryModel)
            .filter_by(
                user_id=user_id,
                session_id=session_id,
                file_name=file_name,
            )
            .first()
        )

    @classmethod
    def update_chat_history(
        cls,
        db: Session,
        user_id: int,
        session_id: UUID,
        file_name: str,
        chat_history_update: ChatHistorySchema,
    ) -> None:
        chat_history = cls.get_chat_history(
            db=db,
            user_id=user_id,
            session_id=session_id,
            file_name=file_name,
        )

        if chat_history is None:
            raise ChatHistoryNotFound(
                f"No chat history for user_id={user_id}, session_id={session_id}, file_name={file_name}"
            )

        if chat_history_update.solutions is not None:
            chat_history.solutions = chat_history_update.solutions

        if chat_history_update.code is not None:
            chat_history.code = chat_history_update.code

        if chat_history_update.variables is not None:
            chat_history.variables = chat_history_update.variables

        if chat_history_update.conversation is not None:
            chat_history.conversation = chat_history_update.conversation

        db.commit()

    @classmethod
    def delete_chat_history(cls, db: Session, user_id: int, file_name: str) -> None:
        """..."""

        (
            db.query(ChatHistoryModel)
            .filter(
                ChatHistoryModel.user_id == user_id,
                ChatHistoryModel.file_name == file_name,
            )
            .delete(synchronize_session=False)
        )
        db.commit()
