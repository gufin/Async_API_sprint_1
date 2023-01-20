from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel

from models.models import UUIDMixin
from services.person import get_person_service, PersonService

router = APIRouter()


class PersonAPI(UUIDMixin, BaseModel):
    full_name: str
    role: str
    film_ids: list[UUID]


class PersonsFilm(UUIDMixin, BaseModel):
    title: str
    imdb_rating: float


class PersonListAPI(UUIDMixin, BaseModel):
    full_name: str


@router.get('/', response_model=list[PersonListAPI])
async def person_list(
        request: Request,
        page_size: int = Query(10, description='Number of films on page'),
        page: int = Query(1, description='Page number'),
        sort: str = Query('',
                          description='Sorting field. '
                                      'Example: imdb_rating:desc'),
        genre: str = Query(None, description='Filter by genre uuid'),
        get_person_service: PersonService = Depends(get_person_service)
) -> list[PersonListAPI]:
    persons = await get_person_service.get_list(page_size=page_size,
                                                page=page,
                                                sort=sort,
                                                genre=genre,
                                                url=request.url._url, )
    return [PersonListAPI.parse_obj(person.dict(by_alias=True)) for person in
            persons]


@router.get('/{person_id}/film', response_model=list[PersonsFilm])
async def person_details(person_id: str,
                         person_service: PersonService = Depends(
                             get_person_service)
                         ) -> list[PersonsFilm]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='person not found')
    films = []
    for film_data in person.films.values():
        for film in film_data:
            person_film = PersonsFilm.parse_obj(film.dict(by_alias=True))
            if person_film not in films:
                films.append(person_film)
    return films


@router.get('/{person_id}', response_model=PersonAPI)
async def person_details(person_id: str,
                         person_service: PersonService = Depends(
                             get_person_service)
                         ) -> PersonAPI:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='person not found')
    film_ids = []
    person_roles = ''
    for role, films in person.films.items():
        if role not in person_roles:
            if len(person_roles) > 0:
                person_roles += ', ' + role
            else:
                person_roles = role
        for film in films:
            if film not in film_ids:
                film_ids.append(film.uuid)
    person_api = PersonAPI(id=person.uuid,
                           full_name=person.full_name,
                           role=person_roles,
                           film_ids=film_ids)
    return person_api
