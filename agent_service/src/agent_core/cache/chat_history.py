"""..."""

from uuid import UUID
from dataclasses import dataclass
from typing import Optional, Type
import pickle

from redis import Redis, RedisError
from sqlalchemy.orm import Session

from schemas.chat_history import ChatHistory as ChatHistorySchema
from agent_core.core.config import settings
from repositories.chat_history import ChatHistoryRepository


@dataclass
class ChatHistoryCacheManager:
    """..."""

    host: str
    port: int
    db: int
    chat_history_repository: Type[ChatHistoryRepository]
    client: Optional[Redis] = None
    default_ttl: int = 3600

    def _ensure_connected(self):
        """..."""
        if self.client is None:
            raise ConnectionError(
                "Redis client is not initialized. Call 'connect_client()' first"
            )

    @staticmethod
    def format_key(session_id: UUID) -> str:
        """..."""
        return f"chat_history:{session_id}"

    def connect_client(self) -> None:
        """..."""
        if self.client is None:
            self.client = Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=False,
                socket_keepalive=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )

    def close_client(self) -> None:
        """..."""
        if self.client:
            try:
                self.client.close()
            except RedisError:
                ...
            finally:
                self.client = None

    def get_chat_history(self, db: Session, session_id: UUID) -> ChatHistorySchema:
        """..."""
        self._ensure_connected()
        key = self.format_key(session_id=session_id)

        try:
            chat_history_bytes = self.client.get(key)
            if chat_history_bytes is not None:
                return pickle.loads(chat_history_bytes)

            # Cache miss: retrieve or create in DB
            db_chat_history = self.chat_history_repository.get_chat_history(
                db=db, session_id=session_id
            )
            if db_chat_history is None:
                db_chat_history = self.chat_history_repository.create_chat_history(
                    db=db, session_id=session_id
                )
                # Make sure this commits in repository method

            chat_history = ChatHistorySchema.model_validate(db_chat_history)
            self.cache_chat_history(session_id=session_id, chat_history=chat_history)
            return chat_history
        except RedisError:
            ...

    def cache_chat_history(
        self, session_id: UUID, chat_history: ChatHistorySchema
    ) -> None:
        """..."""
        self._ensure_connected()
        key = self.format_key(session_id=session_id)
        try:
            chat_history_bytes = pickle.dumps(chat_history)
            self.client.set(key, chat_history_bytes)
            self.client.expire(key, self.default_ttl)
        except RedisError:
            ...


chat_history_cache_manager = ChatHistoryCacheManager(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    db=settings.redis.DB,
    chat_history_repository=ChatHistoryRepository,
)
