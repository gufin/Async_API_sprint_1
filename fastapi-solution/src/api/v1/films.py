from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

import core.constants as constants
from api.v1.models import FilmAPI, FilmList
from services.film import BaseService, get_film_service

router = APIRouter()

@router.get('/search',
            response_model=list[FilmList],
            summary=constants.FILM_SEARCH_LIST_SUMMARY,
            description=constants.FILM_SEARCH_LIST_DESCRIPTION
            )
async def film_search_list(
        request: Request,
        page_size: int = Query(10, description=constants.PAGE_SIZE_DESCRIPTION,
                               ge=1),
        page: int = Query(1, description=constants.PAGE_DESCRIPTION, ge=1),
        sort: constants.FilmsSortingFields = Query('',
                                                   description=constants.SORT_DESCRIPTION),
        query: str = Query(None, description=constants.FILM_SEARCH_DESCRIPTION),
        film_service: BaseService = Depends(get_film_service)
) -> list[FilmList]:
    sort_val = '' if sort == '' else sort.value
    films = await film_service.get_list(page_size=page_size,
                                        page=page,
                                        sort=sort_val,
                                        query=query,
                                        url=request.url._url, )
    return [FilmList.parse_obj(film.dict(by_alias=True)) for film in films]


@router.get('/{film_id}',
            response_model=FilmAPI,
            summary=constants.FILM_ID_SUMMARY,
            description=constants.FILM_ID_DESCRIPTION,
            )
async def film_details(film_id: str,
                       film_service: BaseService = Depends(get_film_service)
                       ) -> FilmAPI:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=constants.FILM_NOT_FOUND)
    return FilmAPI.parse_obj(film.dict(by_alias=True))


@router.get('/',
            response_model=list[FilmList],
            summary=constants.FILM_LIST_SUMMARY,
            description=constants.FILM_LIST_DESCRIPTION
            )
async def film_list(
        request: Request,
        page_size: int = Query(10, description=constants.PAGE_SIZE_DESCRIPTION,
                               ge=1),
        page: int = Query(1, description=constants.PAGE_DESCRIPTION, ge=1),
        sort: constants.FilmsSortingFields = Query('',
                                                   description=constants.SORT_DESCRIPTION),
        genre: str = Query(None,
                           description=constants.GENRE_FILTER_DESCRIPTION),
        query: str = Query(None, description=constants.FILM_SEARCH_DESCRIPTION),
        film_service: BaseService = Depends(get_film_service)
) -> list[FilmList]:
    sort_val = '' if sort == '' else sort.value
    films = await film_service.get_list(page_size=page_size,
                                        page=page,
                                        sort=sort_val,
                                        genre=genre,
                                        url=request.url._url,
                                        query=query)
    return [FilmList.parse_obj(film.dict(by_alias=True)) for film in films]



