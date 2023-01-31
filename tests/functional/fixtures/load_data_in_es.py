import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from testdata.es_data import film_work_data, genres_data, persons_data
from testdata.es_mapping import GENRES_INDEX, MOVIES_INDEX, PERSONS_INDEX


async def write_data_to_elastic(
    es_client: AsyncElasticsearch, index: dict, data: dict
):
    index_name = index["index"]
    if not await es_client.indices.exists(index=index_name):
        await es_client.indices.create(index_name, index["body"])
    bulk_query = []
    for row in data:
        action = {"index": {"_index": index_name, "_id": row["id"]}}
        doc = row
        bulk_query.extend((action, doc))
    response = await es_client.bulk(bulk_query, index_name, refresh=True)
    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")


@pytest_asyncio.fixture(scope="session", autouse=True)
async def es_write_filmworks(es_client):
    await write_data_to_elastic(es_client, MOVIES_INDEX, film_work_data)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def es_write_genres(es_client):
    await write_data_to_elastic(es_client, GENRES_INDEX, genres_data)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def es_write_persons(es_client):
    await write_data_to_elastic(es_client, PERSONS_INDEX, persons_data)
