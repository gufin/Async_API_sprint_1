from aioredis import Redis
from core.config import app_settings
from elasticsearch import AsyncElasticsearch, NotFoundError


class RedisWorker:
    def get_by_id(self, func):
        async def wrapper(cls, service_object_id: str):
            data = await cls.redis.get(service_object_id)
            if data:
                return cls.model.parse_raw(data)
            service_object = await func(cls, service_object_id)
            if service_object:
                await self._put_service_object_to_cache(cls, service_object)
            return service_object

        return wrapper

    def get_list(self, func):
        async def wrapper(
            cls,
            page_size: int,
            page: int,
            sort: str,
            genre: str,
            query: str,
            url: str,
        ):
            if key := self._generate_redis_key(
                page_size, page, sort, genre, url, query
            ):
                data = await cls.redis.lrange(key, 0, -1)
                service_objects = [
                    cls.list_model.parse_raw(item) for item in data
                ]
                if service_objects:
                    return service_objects[::-1]
                service_objects = await func(
                    cls, page_size, page, sort, genre, query, url
                )
                if len(service_objects) > 0:
                    await self._put_list_to_cache(
                        cls,
                        service_objects,
                        page_size,
                        page,
                        sort,
                        genre,
                        url,
                        query,
                    )
                return service_objects

        return wrapper

    @staticmethod
    def _generate_redis_key(
        page_size: int, page: int, sort: str, genre: str, url: str, query: str
    ):
        model_name = url.split("api")[1].split("/")[2]
        return (
            f"api/v1/{model_name}/?page_size={page_size}"
            f"&page={page}&sort={sort if sort else None}&genre={genre}"
            f"&query={query if query else None}"
        )

    @staticmethod
    async def _put_service_object_to_cache(cls, service_object):
        await cls.redis.set(
            str(service_object.uuid),
            service_object.json(by_alias=True),
        )

    async def _put_list_to_cache(
        self,
        cls,
        service_objects: list,
        page_size: int,
        page: int,
        sort: str,
        genre: str,
        url: str,
        query: str,
    ):
        if key := self._generate_redis_key(
            page_size, page, sort, genre, url, query
        ):
            print(key)
            data = [item.json(by_alias=True) for item in service_objects]
            await cls.redis.lpush(
                key,
                *data,
            )
        await cls.redis.expire(key, app_settings.cache_expire_in_seconds)


redis_worker = RedisWorker()


class BaseService:
    def __init__(
        self,
        redis: Redis,
        elastic: AsyncElasticsearch,
        index: str,
        model,
        searching_field: str = "",
        list_model=None,
    ):
        self.redis = redis
        self.elastic = elastic
        self.index = index
        self.model = model
        self.searching_field = searching_field
        self.list_model = list_model or model

    @redis_worker.get_list
    async def get_list(
        self, page_size=10, page=1, sort="", genre=None, query=None, url=None
    ):
        service_objects = await self._get_list_from_elastic(
            page_size, page, sort, genre, query, url
        )
        return service_objects or []

    async def _get_list_from_elastic(
        self, page_size=10, page=1, sort="", genre=None, query=None, url=None
    ):
        body = None
        if genre:
            body = {
                "query": {
                    "query_string": {"default_field": "genre", "query": genre}
                }
            }
        if query:
            body = {
                "query": {
                    "match": {
                        self.searching_field: {
                            "query": query,
                            "fuzziness": 1,
                            "operator": "and",
                        }
                    }
                }
            }
        try:
            docs = await self.elastic.search(
                index=self.index,
                body=body,
                params={
                    "size": page_size,
                    "from": page - 1,
                    "sort": sort,
                },
            )
        except NotFoundError:
            return None
        return [
            self.list_model.parse_obj(doc["_source"])
            for doc in docs["hits"]["hits"]
        ]

    @redis_worker.get_by_id
    async def get_by_id(self, service_object_id: str):
        service_object = await self._get_service_object_from_elastic(
            service_object_id
        )
        return service_object or None

    async def _get_service_object_from_elastic(self, service_object_id: str):
        try:
            doc = await self.elastic.get(self.index, service_object_id)
        except NotFoundError:
            return None
        return self.model.parse_obj(doc["_source"])
