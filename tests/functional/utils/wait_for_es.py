import asyncio

import backoff
from elasticsearch import AsyncElasticsearch
from settings import app_settings
from utils.helpers import backoff_handler


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
    print("Попытка установить соединение с ElasticSearch")

    es = await elastic_connect(
        host=f"{app_settings.elastic_host}:{app_settings.elastic_port}"
    )
    await es.close()
    print("Соединение установлено успешно")


if __name__ == "__main__":
    asyncio.run(main())
