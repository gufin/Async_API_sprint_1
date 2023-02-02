from http import HTTPStatus

import pytest
from testdata.es_data import high_rating

pytestmark = pytest.mark.asyncio


async def test_search_film_fast_api(make_get_request):
    original_film = high_rating[0]

    response = await make_get_request(
        "/films/", params={"query": "High rating title"}
    )
    film = response.body[0]

    assert response.status == HTTPStatus.OK
    for key in film.keys():
        assert film[key] == original_film[key]


async def test_search_film_fast_api_invalid_title(make_get_request):
    response = await make_get_request(
        "/films/", params={"query": "Harry Potter"}
    )

    assert len(response.body) == 0


async def test_search_genre_fast_api(make_get_request):
    response = await make_get_request("/genres/", params={"query": "Thriller"})
    genre = response.body[0]

    assert response.status == HTTPStatus.OK
    assert str(genre["id"]) == "0ee5e6ef-2cd0-49db-8f71-8030f590d220"


async def test_search_genre_fast_api_invalid_name(make_get_request):
    response = await make_get_request("/genres/", params={"query": "Horror"})

    assert len(response.body) == 0


async def test_search_person_fast_api(make_get_request):
    response = await make_get_request(
        "/persons/", params={"query": "Madikhan"}
    )
    person = response.body[0]

    assert response.status == HTTPStatus.OK
    assert str(person["id"]) == "3fa85f64-5717-4562-b3fc-2c963f66afa6"


async def test_search_person_fast_api_invalid_name(make_get_request):
    response = await make_get_request("/persons/", params={"query": "Haryy"})

    assert len(response.body) == 0
