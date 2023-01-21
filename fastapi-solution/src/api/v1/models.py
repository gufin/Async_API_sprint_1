from uuid import UUID

from pydantic import BaseModel

from models.models import GenreBase, PersonBase, UUIDMixin


class FilmAPI(UUIDMixin, BaseModel):
    title: str
    imdb_rating: float
    description: str
    genres: list[GenreBase]
    actors: list[PersonBase]
    writers: list[PersonBase]
    directors: list[PersonBase]


class FilmList(UUIDMixin, BaseModel):
    title: str
    imdb_rating: float


class GenreAPI(UUIDMixin, BaseModel):
    name: str


class PersonAPI(UUIDMixin, BaseModel):
    full_name: str
    role: str
    film_ids: list[UUID]


class PersonsFilm(UUIDMixin, BaseModel):
    title: str
    imdb_rating: float


class PersonListAPI(UUIDMixin, BaseModel):
    full_name: str
