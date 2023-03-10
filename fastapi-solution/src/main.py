import logging

import aioredis
import uvicorn
from aiobreaker import CircuitBreaker, CircuitBreakerListener
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
from httpx import AsyncClient, RequestError

from api.v1 import films, genres, persons
from core.config import app_settings
from db import elastic, redis

app = FastAPI(
    title=app_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = aioredis.from_url(
        app_settings.redis_url, encoding="utf8", decode_responses=True
    )
    elastic.es = AsyncElasticsearch(
        hosts=[f"{app_settings.elastic_host}:{app_settings.elastic_port}"]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])

auth_breaker = CircuitBreaker(fail_max=5)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if app_settings.test_mode:
        return await call_next(request)
    headers = request.headers
    try:
        auth_answer = await send_circuit_request(app_settings.auth_service,
                                                 headers=dict(headers))
    except RequestError:
        return Response(content="Anonymous user",
                        status_code=401)
    if auth_answer.status_code == 200:
        data = auth_answer.json()
        return await call_next(request)
    return Response(content="Anonymous user",
                    status_code=401)


class LogListener(CircuitBreakerListener):
    def state_change(self, breaker, old, new):
        logging.info(f"{old.state} -> {new.state}")


@auth_breaker
async def send_circuit_request(url: str, headers: dict):
    async with AsyncClient() as client:
        answer = await client.get(url, headers=headers)
        logging.info(answer)
        return answer


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
    )
