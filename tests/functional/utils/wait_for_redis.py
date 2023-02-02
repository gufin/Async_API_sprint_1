import asyncio

import aioredis
import backoff
from settings import app_settings
from utils.helpers import backoff_handler


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=app_settings.CONNECTIONS_MAX_TIME,
)
async def redis_connect(*, host: str, port: int) -> aioredis.Redis:
    redis = await aioredis.from_url(f"redis://{host}:{port}")
    pong = await redis.ping()
    if not pong:
        raise ConnectionError("Connection failed")
    return redis


async def main():
    print("Попытка установить соединение с redis")
    redis = await redis_connect(
        host=app_settings.redis_host, port=app_settings.redis_port
    )
    await redis.close()
    print("Соединение установлено успешно")


if __name__ == "__main__":
    asyncio.run(main())
