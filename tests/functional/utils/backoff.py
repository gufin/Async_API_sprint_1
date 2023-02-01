import asyncio
import logging

import aioredis
import backoff
from elasticsearch import AsyncElasticsearch
from settings import app_settings


def backoff_handler(details):
    logging.error(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


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


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=app_settings.CONNECTIONS_MAX_TIME,
)
async def elastic_connect(*, host: str) -> AsyncElasticsearch:
    elastic = AsyncElasticsearch(hosts=host, verify_certs=True)
    if not await elastic.ping():
        raise ConnectionError("Connection failed")
    return elastic


async def main():
    print('Попытка установить соединение с ES и redis')

    es = await elastic_connect(host=f"{app_settings.elastic_host}:{app_settings.elastic_port}")
    await es.close()

    redis = await redis_connect(host=app_settings.redis_host, port=app_settings.redis_port)
    await redis.close()
    print('Соединение установлено успешно')


if __name__ == "__main__":
    asyncio.run(main())
