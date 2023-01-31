from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

import core.constants as constants
from api.v1.models import PersonAPI, PersonListAPI, PersonsFilm
from services.person import BaseService, get_person_service

router = APIRouter()


@router.get('/',
            response_model=list[PersonListAPI],
            summary=constants.PERSON_LIST_SUMMARY,
            description=constants.PERSON_LIST_DESCRIPTION
            )
async def person_list(
        request: Request,
        page_size: int = Query(10, description=constants.PAGE_SIZE_DESCRIPTION,
                               ge=1),
        page: int = Query(1, description=constants.PAGE_DESCRIPTION, ge=1),
        sort: str = Query('', description=constants.SORT_DESCRIPTION),
        genre: str = Query(None,
                           description=constants.GENRE_FILTER_DESCRIPTION),
        get_person_service: BaseService = Depends(get_person_service)
) -> list[PersonListAPI]:
    persons = await get_person_service.get_list(page_size=page_size,
                                                page=page,
                                                sort=sort,
                                                genre=genre,
                                                url=request.url._url,
                                                query=None,)
    return [PersonListAPI.parse_obj(person.dict(by_alias=True)) for person in
            persons]


@router.get('/search',
            response_model=list[PersonListAPI],
            summary=constants.PERSON_SEARCH_LIST_SUMMARY,
            description=constants.PERSON_SEARCH_LIST_DESCRIPTION
            )
async def person_list(
        request: Request,
        page_size: int = Query(10, description=constants.PAGE_SIZE_DESCRIPTION,
                               ge=1),
        page: int = Query(1, description=constants.PAGE_DESCRIPTION, ge=1),
        sort: str = Query('', description=constants.SORT_DESCRIPTION),
        genre: str = Query(None,
                           description=constants.GENRE_FILTER_DESCRIPTION),
        query: str = Query(None,
                           description=constants.PERSON_SEARCH_DESCRIPTION),
        get_person_service: BaseService = Depends(get_person_service)
) -> list[PersonListAPI]:
    persons = await get_person_service.get_list(page_size=page_size,
                                                page=page,
                                                sort=sort,
                                                genre=genre,
                                                query=query,
                                                url=request.url._url, )
    return [PersonListAPI.parse_obj(person.dict(by_alias=True)) for person in
            persons]


@router.get('/{person_id}/film',
            response_model=list[PersonsFilm],
            summary=constants.PERSON_FILMS_SUMMARY,
            description=constants.PERSON_FILMS_DESCRIPTION
            )
async def person_details(person_id: str,
                         person_service: BaseService = Depends(
                             get_person_service)
                         ) -> list[PersonsFilm]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=constants.PERSON_NOT_FOUND)
    films = []
    for film_data in person.films.values():
        for film in film_data:
            person_film = PersonsFilm.parse_obj(film.dict(by_alias=True))
            if person_film not in films:
                films.append(person_film)
    return films


@router.get('/{person_id}',
            response_model=PersonAPI,
            summary=constants.PERSON_ID_SUMMARY,
            description=constants.PERSON_ID_DESCRIPTION,
            )
async def person_details(person_id: str,
                         person_service: BaseService = Depends(
                             get_person_service)
                         ) -> PersonAPI:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=constants.PERSON_NOT_FOUND)
    film_ids = []
    person_roles = ''
    for role, films in person.films.items():
        if role not in person_roles:
            if len(person_roles) > 0:
                person_roles += f', {role}'
            else:
                person_roles = role
        for film in films:
            if film not in film_ids:
                film_ids.append(film.uuid)
    return PersonAPI(id=person.uuid, full_name=person.full_name,
                     role=person_roles, film_ids=film_ids)
