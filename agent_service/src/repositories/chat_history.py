"""..."""

from uuid import UUID
from typing import Optional
import pickle

from sqlalchemy.orm import Session

from schemas.chat_history import ChatHistory as ChatHistorySchema
from models.chat_history import ChatHistory as ChatHistoryModel


class ChatHistoryRepository:
    """..."""

    @classmethod
    def get_chat_history(
        cls, db: Session, session_id: UUID
    ) -> Optional[ChatHistoryModel]:
        """..."""
        chat_history = (
            db.query(ChatHistoryModel)
            .filter(ChatHistoryModel.session_id == session_id)
            .first()
        )
        return chat_history

    @classmethod
    def create_chat_history(cls, db: Session, session_id: UUID) -> ChatHistoryModel:
        """..."""
        chat_history = ChatHistorySchema(
            session_id=session_id,
            solutions=pickle.dumps([]),
            code=pickle.dumps(""),
            variables=pickle.dumps({}),
        )
        db_chat_history = ChatHistoryModel(**chat_history.model_dump())
        db.add(db_chat_history)
        db.commit()
        db.refresh(db_chat_history)
        return db_chat_history

    @classmethod
    def update_chat_history(
        cls, db: Session, session_id: UUID, chat_history: ChatHistorySchema
    ) -> ChatHistoryModel:
        """..."""
        db_chat_history = cls.get_chat_history(db=db, session_id=session_id)
        if db_chat_history is None:
            raise FileNotFoundError(
                f"No chat history found for session_id={session_id}"
            )
        update_data = chat_history.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_chat_history, field, value)
        db.commit()
        db.refresh(db_chat_history)
        return db_chat_history

    @classmethod
    def delete_chat_history(cls, db: Session, session_id: UUID) -> None:
        """..."""
        db_chat_history = cls.get_chat_history(db=db, session_id=session_id)
        if db_chat_history is None:
            raise FileNotFoundError(
                f"No chat history found for session_id={session_id}"
            )
        db.delete(db_chat_history)
        db.commit()
