from redis.asyncio import ConnectionPool, Redis
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError
from redis.retry import Retry

from backend.env_loader import EnvLoader


class RedisClient:
    def __init__(self) -> None:
        self.__connection_pool = ConnectionPool(
            host=EnvLoader.get("REDIS_HOST"),
            port=int(EnvLoader.get("REDIS_PORT")),
            username=EnvLoader.get("REDIS_USERNAME"),
            password=EnvLoader.get("REDIS_PASSWORD"),
            decode_responses=True,
            socket_keepalive=True,
            socket_timeout=5,
            socket_connect_timeout=5,
            health_check_interval=30,  # pings periodically to detect dead conns
            retry=Retry(
                ExponentialBackoff(),
                retries=5,
                supported_errors=(TimeoutError, ConnectionError),
            ),  # retries on disconnect
        )
        self.client = Redis(
            connection_pool=self.__connection_pool,
            decode_responses=True,
        )
