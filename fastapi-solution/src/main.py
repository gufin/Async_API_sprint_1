import aioredis
import gunicorn as gunicorn
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core.config import app_settings
from db import elastic, redis

app = FastAPI(
    title=app_settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (app_settings.redis_host, app_settings.redis_port), minsize=10, maxsize=20)
    elastic.es = AsyncElasticsearch(
        hosts=[f'{app_settings.elastic_host}:{app_settings.elastic_port}'])


@app.on_event('shutdown')
async def shutdown():
    redis.redis.close()
    await redis.redis.wait_closed()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])
app.include_router(persons.router, prefix='/api/v1/persons', tags=['persons'])
app.include_router(genres.router, prefix='/api/v1/genres', tags=['genres'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8001,
    )
