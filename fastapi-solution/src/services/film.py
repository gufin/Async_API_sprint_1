from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import app_settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.models import FilmWork


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_list(self, **kwargs) -> Optional[list[FilmWork]]:
        films = await self._list_from_cache(**kwargs)
        if not films:
            films = await self._get_list_from_elastic(**kwargs)
            if not films:
                return []
            await self._put_list_to_cache(films, **kwargs)
        return films

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
            docs = await self.elastic.search(index='movies',
                                             body=body,
                                             params={
                                                 'size': page_size,
                                                 'from': page - 1,
                                                 'sort': sort,
                                             })
        except NotFoundError:
            return None
        return [FilmWork.parse_obj(doc['_source']) for doc in
                docs['hits']['hits']]

    async def get_by_id(self, film_id: str) -> Optional[FilmWork]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[FilmWork]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return FilmWork.parse_obj(doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[FilmWork]:
        data = await self.redis.get(film_id)
        return FilmWork.parse_raw(data) if data else None

    async def _put_film_to_cache(self, film: FilmWork):
        await self.redis.set(
            film.uuid, film.json(), expire=app_settings.CACHE_EXPIRE_IN_SECONDS,
        )

    async def _list_from_cache(self, **kwargs) -> list[Optional[FilmWork]]:
        if url := kwargs.get('url'):
            data = await self.redis.lrange(url, 0, -1)
            films = [FilmWork.parse_raw(item) for item in data]
            return films[::-1] if films else []
        return []

    async def _put_list_to_cache(self, films: list, **kwargs):
        if url := kwargs.get('url'):
            data = [item.json() for item in films]
            await self.redis.lpush(
                url, *data,
            )
            await self.redis.expire(url, app_settings.CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
