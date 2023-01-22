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
    age_limit: int | None = 18
    imdb_rating: float
    genres: list[GenreBase]
    description: str | None
    directors_names: list[str | None]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[PersonBase]
    writers: list[PersonBase]
    directors: list[PersonBase]
