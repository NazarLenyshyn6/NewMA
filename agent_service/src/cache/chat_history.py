"""..."""

from uuid import UUID
from dataclasses import dataclass
from typing import Optional
import pickle

from redis import Redis, RedisError

from core.config import settings
from schemas.chat_history import ChatHistory


@dataclass
class ChatHistoryCacheManager:
    """..."""

    host: str
    port: int
    db: int
    client: Optional[Redis] = None
    default_ttl: int = 3600

    def _ensure_connected(self):
        """..."""
        if self.client is None:
            raise ConnectionError(
                "Redis client is not initialized. Call 'connect_client()' first"
            )

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

    @staticmethod
    def format_key(session_id: UUID, file_name: str) -> str:
        """..."""
        return f"chat_history:session:{session_id}:file:{file_name}"

    def get_chat_history(
        self, session_id: UUID, file_name: str
    ) -> Optional[ChatHistory]:
        """..."""
        self._ensure_connected()
        key = self.format_key(session_id, file_name)
        try:
            file_data_bytes = self.client.get(key)
            if file_data_bytes:
                self.client.expire(key, self.default_ttl)
                return pickle.loads(file_data_bytes)
            return file_data_bytes
        except RedisError:
            ...

    def cache_chat_history(
        self, session_id: UUID, file_name: str, chat_history: ChatHistory
    ) -> None:
        """..."""
        self._ensure_connected()
        key = self.format_key(session_id, file_name)
        try:
            chat_history_bytes = pickle.dumps(chat_history)
            self.client.set(key, chat_history_bytes)
            self.client.expire(key, self.default_ttl)
        except RedisError:
            ...


chat_history_cache = ChatHistoryCacheManager(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    db=settings.redis.DB,
)
