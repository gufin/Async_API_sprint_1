import json
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.models import FilmWork
from services.utils import BaseService


async def get_key_by_args(*args, **kwargs) -> str:
    return f'{args}:{json.dumps({"kwargs": kwargs}, sort_keys=True)}'


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> BaseService:
    return BaseService(redis, elastic, 'movies', FilmWork)
