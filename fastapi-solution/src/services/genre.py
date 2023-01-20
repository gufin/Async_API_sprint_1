from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from core.config import app_settings
from db.elastic import get_elastic
from db.redis import get_redis
from models.models import GenreBase


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_list(self, **kwargs) -> Optional[list[GenreBase]]:
        genres = await self._list_from_cache(**kwargs)
        if not genres:
            genres = await self._get_list_from_elastic(**kwargs)
            if not genres:
                return []
            await self._put_list_to_cache(genres, **kwargs)
        return genres

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
            docs = await self.elastic.search(index='genres',
                                             body=body,
                                             params={
                                                 'size': page_size,
                                                 'from': page - 1,
                                                 'sort': sort,
                                             })
        except NotFoundError:
            return None
        return [GenreBase.parse_obj(doc['_source']) for doc in
                docs['hits']['hits']]

    async def get_by_id(self, genre_id: str) -> Optional[GenreBase]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def _get_genre_from_elastic(self,
                                      genre_id) -> Optional[GenreBase]:
        try:
            doc = await self.elastic.get('genres', genre_id)
        except NotFoundError:
            return None
        return GenreBase.parse_obj(doc['_source'])

    async def _genre_from_cache(self,
                                genre_id: str) -> Optional[GenreBase]:
        data = await self.redis.get(genre_id)
        return GenreBase.parse_raw(data) if data else None

    async def _put_genre_to_cache(self, genre: GenreBase) -> None:
        await self.redis.set(
            genre.uuid, genre.json(by_alias=True), expire=app_settings.CACHE_EXPIRE_IN_SECONDS,
        )

    async def _list_from_cache(self, **kwargs) -> list[Optional[GenreBase]]:
        if url := kwargs.get('url'):
            data = await self.redis.lrange(url, 0, -1)
            genres = [GenreBase.parse_raw(item) for item in data]
            return genres[::-1] if genres else []
        return []

    async def _put_list_to_cache(self, genres: list[GenreBase], **kwargs):
        if url := kwargs.get('url'):
            data = [item.json(by_alias=True) for item in genres]
            await self.redis.lpush(
                url, *data,
            )
            await self.redis.expire(url, app_settings.CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
