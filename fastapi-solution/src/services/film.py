from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.models import FilmWork, GenreBase, PersonBase

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


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
            await self._put_list_to_cahe(films)
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
            # logger.debug('An error occurred while trying to get films in ES)')
            return None
        return [await self._make_film_from_es_doc(doc) for doc in
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
        data = doc['_source']
        film = FilmWork(id=data['id'],
                        imdb_rating=data['imdb_rating'],
                        title=data['title'],
                        description=data['description'],
                        directors_names=data['directors_names'],
                        actors_names=data['actors_names'],
                        writers_names=data['writers_names'],
                        actors=self._get_persons_list(data['actors']),
                        writers=self._get_persons_list(data['writers']),
                        genres=self._get_genres_list(data['genres']),
                        directors=self._get_persons_list(data['directors']),
                        )
        return film

    @staticmethod
    def _get_persons_list(persons: list):
        return [PersonBase(**person) for person in persons]

    @staticmethod
    def _get_genres_list(genres: list):
        return [GenreBase(**genre) for genre in genres]

    async def _make_film_from_es_doc(self, doc: dict) -> FilmWork:
        data = doc['_source']
        film = FilmWork(id=data['id'],
                        imdb_rating=data['imdb_rating'],
                        title=data['title'],
                        description=data['description'],
                        directors_names=data['directors_names'],
                        actors_names=data['actors_names'],
                        writers_names=data['writers_names'],
                        actors=self._get_persons_list(data['actors']),
                        writers=self._get_persons_list(data['writers']),
                        genres=self._get_genres_list(data['genres']),
                        directors=self._get_persons_list(data['directors']),
                        )
        return film

    async def _film_from_cache(self, film_id: str) -> Optional[FilmWork]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        #film = FilmWork.parse_raw(data)
        return None

    async def _put_film_to_cache(self, film: FilmWork):
        await self.redis.set(str(film.uuid), film.json(),
                             expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _list_from_cache(self, **kwargs):
        pass

    async def _put_list_to_cache(self, films: list):
        pass


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
