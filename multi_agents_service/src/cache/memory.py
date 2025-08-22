"""..."""

from uuid import UUID
from dataclasses import dataclass
from typing import Optional, TypeVar, Generic
import pickle

from redis import Redis, RedisError

from core.config import settings
from schemas.memory import BaseMemory as BaseMemorySchema

S = TypeVar("S", bound=BaseMemorySchema)


@dataclass
class BaseMemoryCache(Generic[S]):
    """..."""

    host: str
    port: int
    db: int
    key: str
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

    def format_key(self, session_id: UUID, file_name: str) -> str:
        """..."""
        return f"agent_memory:{self.key}:session:{session_id}:file:{file_name}"

    def get_memory(self, session_id: UUID, file_name: str) -> Optional[S]:
        """..."""
        self._ensure_connected()
        key = self.format_key(session_id, file_name)
        try:
            memory_bytes = self.client.get(key)
            if memory_bytes:
                self.client.expire(key, self.default_ttl)
                return pickle.loads(memory_bytes)
            return memory_bytes
        except RedisError:
            ...

    def cache_memory(self, session_id: UUID, file_name: str, memory_schema: S):
        """..."""
        self._ensure_connected()
        key = self.format_key(session_id, file_name)
        try:
            memory_bytes = pickle.dumps(memory_schema)
            self.client.set(key, memory_bytes)
            self.client.expire(key, self.default_ttl)
        except RedisError:
            ...


conversation_summary_memory_cache = BaseMemoryCache(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    db=settings.redis.DB,
    key="conversation_summary_memory",
)

conversation_memory_cache = BaseMemoryCache(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    db=settings.redis.DB,
    key="conversation_memory",
)

code_summary_memory_cache = BaseMemoryCache(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    db=settings.redis.DB,
    key="code_summary_memory",
)

variables_memory_cache = BaseMemoryCache(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    db=settings.redis.DB,
    key="variables_memory",
)
