import json
from http import HTTPStatus

import pytest
from testdata.es_data import high_rating

pytestmark = pytest.mark.asyncio


async def test_film_fast_api(make_get_request):
    original_film = high_rating[0]
    film_id = original_film["id"]

    response = await make_get_request(f"/films/{film_id}")
    film = response.body

    assert response.status == HTTPStatus.OK
    for key in film.keys():
        assert film[key] == original_film[key]


async def test_film_fast_api_invalid_id(make_get_request):
    response = await make_get_request("/films/random_id")

    assert response.status == HTTPStatus.NOT_FOUND


async def test_films_fast_api(make_get_request):
    response = await make_get_request("/films/")
    film = response.body[0]

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 10
    assert film["id"]


async def test_films_desc_sorting(make_get_request):
    response = await make_get_request(
        "/films/", params={"sort": "imdb_rating:desc"}
    )
    first_obj = response.body[0]

    assert response.status == HTTPStatus.OK
    assert first_obj["imdb_rating"] == 9.3
    assert first_obj["title"] == "High rating title"


async def test_films_asc_sorting(make_get_request):
    response = await make_get_request(
        "/films/", params={"sort": "imdb_rating:asc"}
    )
    first_obj = response.body[0]

    assert response.status == HTTPStatus.OK
    assert first_obj["imdb_rating"] == 3.5
    assert first_obj["title"] == "Low rating title"


async def test_films_sort_by_inappropriate_field(make_get_request):
    response = await make_get_request("/films/", params={"sort": "new_sort"})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_films_pagination(make_get_request):
    response = await make_get_request(
        endpoint="/films/", params={"page_size": 15}
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 15


async def test_film_redis(redis_client):
    original_film = high_rating[0]
    film_id = original_film["id"]

    film = await redis_client.get(film_id)
    film = json.loads(film)

    for key, v in original_film.items():
        assert film[key] == v


async def test_films_redis(redis_client):
    page_size = 10
    params = {
        "page_size": page_size,
        "page": 1,
        "sort": None,
        "genre": None,
        "model_name": "films",
        "query": None,
    }
    key = (
        f'api/v1/{params["model_name"]}/?page_size={params["page_size"]}'
        f'&page={params["page"]}&sort={params["sort"]}&genre={params["genre"]}'
        f'&query={params["query"]}'
    )

    data = await redis_client.lrange(key, 0, -1)
    assert data
