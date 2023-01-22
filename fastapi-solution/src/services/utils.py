from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError

from core.config import app_settings


class BaseService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch, index: str,
                 model, list_model=None):
        self.redis = redis
        self.elastic = elastic
        self.index = index
        self.model = model
        self.list_model = model if list_model is None else list_model

    async def get_list(self, **kwargs):
        service_objects = await self._list_from_cache(**kwargs)
        if not service_objects:
            service_objects = await self._get_list_from_elastic(**kwargs)
            if not service_objects:
                return []
            await self._put_list_to_cache(service_objects, **kwargs)
        return service_objects

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
            docs = await self.elastic.search(index=self.index,
                                             body=body,
                                             params={
                                                 'size': page_size,
                                                 'from': page - 1,
                                                 'sort': sort,
                                             })
        except NotFoundError:
            return None
        return [self.list_model.parse_obj(doc['_source']) for doc in
                docs['hits']['hits']]

    async def get_by_id(self, service_object_id: str):
        service_object = await self._service_object_from_cache(
            service_object_id)
        if not service_object:
            service_object = await self._get_service_object_from_elastic(
                service_object_id)
            if not service_object:
                return None
            await self._put_service_object_to_cache(service_object)

        return service_object

    async def _get_service_object_from_elastic(self, service_object_id: str):
        try:
            doc = await self.elastic.get(self.index, service_object_id)
        except NotFoundError:
            return None
        return self.model.parse_obj(doc['_source'])

    async def _service_object_from_cache(self, service_object_id: str):
        data = await self.redis.get(service_object_id)
        return self.model.parse_raw(data) if data else None

    async def _put_service_object_to_cache(self, service_object):
        await self.redis.set(
            str(service_object.uuid), service_object.json(by_alias=True),
            expire=app_settings.CACHE_EXPIRE_IN_SECONDS,
        )

    @staticmethod
    def _generate_redis_key(params: dict):
        if url := params.get('url'):
            model_name = url.split('api')[1].split('/')[2]
            page = params.get('page', 1)
            page_size = params.get('page_size', 10)
            sort = params.get('sort') or None
            genre = params.get('genre') or None
            return (
                f'api/v1/{model_name}/?page_size=&{page_size}'
                f'&page={page}&sort={sort}&genre={genre}'
            )
        return None

    async def _list_from_cache(self, **kwargs):
        if key := self._generate_redis_key(params=kwargs):
            data = await self.redis.lrange(key, 0, -1)
            service_objects = [self.list_model.parse_raw(item) for item in data]
            return service_objects[::-1] if service_objects else []
        return []

    async def _put_list_to_cache(self, service_objects: list, **kwargs):
        if key := self._generate_redis_key(params=kwargs):
            data = [item.json(by_alias=True) for item in service_objects]
            await self.redis.lpush(
                key, *data,
            )
            await self.redis.expire(key, app_settings.CACHE_EXPIRE_IN_SECONDS)
