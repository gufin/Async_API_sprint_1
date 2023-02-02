from http import HTTPStatus

import pytest
from testdata.es_data import persons_data

pytestmark = pytest.mark.asyncio


async def test_person_fast_api(make_get_request):
    person = persons_data[-1]
    person_id = person.get("id")

    response = await make_get_request(f"/persons/{person_id}/")

    assert response.status == HTTPStatus.OK
    assert response.body.get("id") == person_id
    assert response.body.get("full_name") == person.get("full_name")


async def test_persons_fast_api_invalid_id(make_get_request):
    response = await make_get_request("/persons/random_id")

    assert response.status == HTTPStatus.NOT_FOUND


async def test_persons_fast_api(make_get_request):
    response = await make_get_request("/persons/")
    person = response.body[0]

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 10
    assert person["id"]


@pytest.mark.parametrize(
    "page, page_size, expected_count",
    [
        (1, 1, 1),
        (1, 10, 10),
        (2, 10, 10),
    ],
)
async def test_persons_pagination(
    make_get_request, page, page_size, expected_count
):
    response = await make_get_request(
        "/persons/", params={"page": page, "page_size": page_size}
    )

    assert response.status == HTTPStatus.OK
    assert len(response.body) == expected_count


async def test_persons_sorting_by_inappropriate_field(make_get_request):
    response = await make_get_request("/genres/", params={"sort": "unknown"})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_person_redis(redis_client):
    person = persons_data[-1]
    person_id = person.get("id")

    cache = await redis_client.get(person_id)
    assert cache


async def test_persons_redis(redis_client):
    page_size = 10
    params = {
        "page_size": page_size,
        "page": 1,
        "sort": None,
        "genre": None,
        "model_name": "persons",
        "query": None,
    }
    key = (
        f'api/v1/{params["model_name"]}/?page_size={params["page_size"]}'
        f'&page={params["page"]}&sort={params["sort"]}&genre={params["genre"]}'
        f'&query={params["query"]}'
    )

    data = await redis_client.lrange(key, 0, -1)

    assert data
