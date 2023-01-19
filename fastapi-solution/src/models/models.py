from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel
from pydantic.fields import Field


def orjson_dumps(v, *, default):
    """orjson.dumps возвращает bytes, а pydantic требует unicode"""
    return orjson.dumps(v, default=default).decode()


class FastJson(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UUIDMixin(FastJson):
    uuid: UUID = Field(..., alias="id")


class FilmBase(UUIDMixin):
    title: str
    imdb_rating: Optional[float] = 0.0


class GenreBase(UUIDMixin):
    name: str


class PersonBase(UUIDMixin):
    full_name: str


class PersonFilms(PersonBase):
    full_name: str
    films: dict[str, list[FilmBase]] = []


class FilmWork(FilmBase):
    age_limit: Optional[int] = 18
    imdb_rating: float
    genres: list[GenreBase]
    description: str | None
    directors_names: list[str | None]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[PersonBase]
    writers: list[PersonBase]
    directors: list[PersonBase]


"""

person_film = PersonFilms(
    **{
        "id": "e039eedf-4daf-452a-bf92-a0085c68e156",
        "full_name": "Peter Cushing",
        "films": {
            "actor": [
                {
                    "id": "73ecd1e6-6326-405a-b51b-69008f383b72",
                    "title": "Lego Star Wars: The Complete Saga",
                    "imdb_rating": 8.5,
                },
            ],
        },
    }
)
film = FilmWork(
    **{
        "id": "4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f",
        "imdb_rating": 7.9,
        "age_limit": 18,
        "genres": [
            {
                "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
                "name": "Adventure",
            },
            {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
            {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
        ],
        "title": "Star Trek",
        "description": "On the day of James Kirk's birth, his father dies on his damaged starship in a last stand against a Romulan mining vessel looking for Ambassador Spock, who in this time, has grown on Vulcan disdained by his neighbors for his half-human heritage. 25 years later, James T. Kirk has grown into a young rebellious troublemaker. Challenged by Captain Christopher Pike to realize his potential in Starfleet, he comes to annoy academy instructors like Commander Spock. Suddenly, there is an emergency on Vulcan and the newly-commissioned USS Enterprise is crewed with promising cadets like Nyota Uhura, Hikaru Sulu, Pavel Chekov and even Kirk himself, thanks to Leonard McCoy's medical trickery. Together, this crew will have an adventure in the final frontier where the old legend is altered forever as a new version of the legend begins.",
        "directors_names": ["J.J. Abrams"],
        "actors_names": [
            "Chris Pine",
            "Eric Bana",
            "Leonard Nimoy",
            "Zachary Quinto",
        ],
        "writers_names": ["Alex Kurtzman", "Gene Roddenberry", "Roberto Orci"],
        "actors": [
            {
                "id": "5a3d0299-2df2-4070-9fda-65ff4dfa863c",
                "full_name": "Leonard Nimoy",
            },
            {
                "id": "8a34f121-7ce6-4021-b467-abec993fc6cd",
                "full_name": "Zachary Quinto",
            },
            {
                "id": "959d148c-022b-427f-a68b-bbe58674fe65",
                "full_name": "Eric Bana",
            },
            {
                "id": "9f38323f-5912-40d2-a90c-b56899746f2a",
                "full_name": "Chris Pine",
            },
        ],
        "writers": [
            {
                "id": "6960e2ca-889f-41f5-b728-1e7313e54d6c",
                "full_name": "Gene Roddenberry",
            },
            {
                "id": "82b7dffe-6254-4598-b6ef-5be747193946",
                "full_name": "Alex Kurtzman",
            },
            {
                "id": "9b58c99a-e5a3-4f24-8f67-a038665758d6",
                "full_name": "Roberto Orci",
            },
        ],
        "directors": [
            {
                "id": "a1758395-9578-41af-88b8-3f9456e6d938",
                "full_name": "J.J. Abrams",
            }
        ],
    }
)
"""
