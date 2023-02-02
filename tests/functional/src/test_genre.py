from http import HTTPStatus

import pytest
from testdata.es_data import genres_data

pytestmark = pytest.mark.asyncio


async def test_genre_fast_api(make_get_request):
    genre = genres_data[-1]
    genre_id = genre.get("id")

    response = await make_get_request(f"/genres/{genre_id}/")

    assert response.status == HTTPStatus.OK
    assert response.body.get("id") == genre_id
    assert response.body.get("name") == genre.get("name")


async def test_genre_fast_api_invalid_id(make_get_request):
    response = await make_get_request("/genres/random_id")

    assert response.status == HTTPStatus.NOT_FOUND


async def test_genres_fast_api(make_get_request):
    response = await make_get_request("/genres/")

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 10


@pytest.mark.parametrize(
    "page, page_size, expected_count",
    [
        (1, 1, 1),
        (1, 10, 10),
        (2, 10, 10),
    ],
)
async def test_genres_pagination(
    make_get_request, page, page_size, expected_count
):
    response = await make_get_request(
        "/genres/", params={"page": page, "page_size": page_size}
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body) == expected_count


async def test_genre_sorting_by_inappropriate_field(make_get_request):
    response = await make_get_request("/genres/", params={"sort": "unknown"})
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_genre_redis(redis_client):
    genre = genres_data[-1]
    genre_id = genre.get("id")

    cache = await redis_client.get(genre_id)
    assert cache


async def test_genres_redis(redis_client):
    page_size = 10
    params = {
        "page_size": page_size,
        "page": 1,
        "sort": None,
        "genre": None,
        "model_name": "genres",
        "query": None,
    }
    key = (
        f'api/v1/{params["model_name"]}/?page_size={params["page_size"]}'
        f'&page={params["page"]}&sort={params["sort"]}&genre={params["genre"]}'
        f'&query={params["query"]}'
    )

    data = await redis_client.lrange(key, 0, -1)
    assert data
