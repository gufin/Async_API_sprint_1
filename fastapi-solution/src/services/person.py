from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import app_settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.models import PersonBase, PersonFilms


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_list(self, **kwargs) -> Optional[list[PersonBase]]:
        persons = await self._list_from_cache(**kwargs)
        if not persons:
            persons = await self._get_list_from_elastic(**kwargs)
            if not persons:
                return []
            await self._put_list_to_cache(persons, **kwargs)
        return persons

    async def _get_list_from_elastic(self, **kwargs):
        page_size = kwargs.get('page_size', 10)
        page = kwargs.get('page', 1)
        sort = kwargs.get('sort', '')
        genre = kwargs.get('genre', None)
        query = kwargs.get('query', None)
        body = None
        if genre:
            body = {
                'query': {
                    'query_string': {
                        'default_field': 'genre',
                        'query': genre
                    }
                }
            }
        if query:
            body = {
                'query': {
                    'match': {
                        'title': {
                            'query': query,
                            'fuzziness': 1,
                            'operator': 'and'
                        }
                    }
                }
            }
        try:
            docs = await self.elastic.search(index='persons',
                                             body=body,
                                             params={
                                                 'size': page_size,
                                                 'from': page - 1,
                                                 'sort': sort,
                                             })
        except NotFoundError:
            return None
        return [PersonBase.parse_obj(doc['_source']) for doc in
                docs['hits']['hits']]

    async def get_by_id(self, person_id: str) -> Optional[PersonFilms]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def _get_person_from_elastic(self,
                                       person_id) -> Optional[PersonFilms]:
        try:
            doc = await self.elastic.get('persons', person_id)
        except NotFoundError:
            return None
        return PersonFilms.parse_obj(doc['_source'])

    async def _person_from_cache(self,
                                 person_id: str) -> Optional[PersonFilms]:
        data = await self.redis.get(person_id)
        return PersonFilms.parse_raw(data) if data else None

    async def _put_person_to_cache(self, person: PersonFilms) -> None:
        await self.redis.set(
            person.uuid, person.json(), expire=app_settings.CACHE_EXPIRE_IN_SECONDS,
        )

    async def _list_from_cache(self, **kwargs) -> list[Optional[PersonFilms]]:
        if url := kwargs.get('url'):
            data = await self.redis.lrange(url, 0, -1)
            persons = [PersonFilms.parse_raw(item) for item in data]
            return persons[::-1] if persons else []
        return []

    async def _put_list_to_cache(self, persons: list, **kwargs):
        if url := kwargs.get('url'):
            data = [item.json() for item in persons]
            await self.redis.lpush(
                url, *data,
            )
            await self.redis.expire(url, app_settings.CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
