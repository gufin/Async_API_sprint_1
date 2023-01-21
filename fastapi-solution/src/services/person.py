from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.models import PersonBase, PersonFilms
from services.utils import BaseService


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> BaseService:
    return BaseService(redis, elastic, 'persons', PersonFilms, PersonBase)
