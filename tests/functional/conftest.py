import asyncio
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy
from settings import app_settings as test_settings


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


pytest_plugins = [
    "fixtures.load_data_in_es",
]


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def es_client():
    async with AsyncElasticsearch(hosts=[test_settings.elastic_url]) as client:
        yield client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def redis_client():
    client = await aioredis.from_url(
        test_settings.redis_url, encoding="utf-8", decode_responses=True
    )
    yield client
    client.close()


@pytest.fixture
def make_get_request(session):
    async def inner(endpoint: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = f"{test_settings.service_api_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return HTTPResponse(
                    body=await response.json(),
                    headers=response.headers,
                    status=response.status,
                )

    return inner
