from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

import core.constants as constants
from api.v1.models import GenreAPI
from services.genre import BaseService, get_genre_service

router = APIRouter()


@router.get('/',
            response_model=list[GenreAPI],
            summary=constants.GENRE_LIST_SUMMARY,
            description=constants.GENRE_LIST_DESCRIPTION
            )
async def genre_list(
        request: Request,
        page_size: int = Query(10, description=constants.PAGE_SIZE_DESCRIPTION,
                               ge=1),
        page: int = Query(1, description=constants.PAGE_DESCRIPTION, ge=1),
        sort: constants.GenreSortingFields = Query('', description=constants.SORT_DESCRIPTION),
        genre: str = Query(None,
                           description=constants.GENRE_FILTER_DESCRIPTION),
        get_genre_service: BaseService = Depends(get_genre_service)
) -> list[GenreAPI]:
    genres = await get_genre_service.get_list(page_size=page_size,
                                              page=page,
                                              sort=sort,
                                              genre=genre,
                                              url=request.url._url,
                                              query=None,)
    return [GenreAPI.parse_obj(genre.dict(by_alias=True)) for genre in
            genres]


@router.get('/search',
            response_model=list[GenreAPI],
            summary=constants.GENRE_SEARCH_LIST_SUMMARY,
            description=constants.GENRE_SEARCH_LIST_DESCRIPTION
            )
async def genre_list(
        request: Request,
        page_size: int = Query(10, description=constants.PAGE_SIZE_DESCRIPTION,
                               ge=1),
        page: int = Query(1, description=constants.PAGE_DESCRIPTION, ge=1),
        sort: str = Query('', description=constants.SORT_DESCRIPTION),
        genre: str = Query(None,
                           description=constants.GENRE_FILTER_DESCRIPTION),
        query: str = Query(None,
                           description=constants.GENRE_SEARCH_DESCRIPTION),
        get_genre_service: BaseService = Depends(get_genre_service)
) -> list[GenreAPI]:
    genres = await get_genre_service.get_list(page_size=page_size,
                                              page=page,
                                              sort=sort,
                                              genre=genre,
                                              query=query,
                                              url=request.url._url, )
    return [GenreAPI.parse_obj(genre.dict(by_alias=True)) for genre in
            genres]


@router.get('/{genre_id}',
            response_model=GenreAPI,
            summary=constants.GENRE_ID_SUMMARY,
            description=constants.GENRE_ID_DESCRIPTION
            )
async def genre_details(genre_id: str,
                        genre_service: BaseService = Depends(
                            get_genre_service)
                        ) -> GenreAPI:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=constants.GENRE_NOT_FOUND)

    return GenreAPI.parse_obj(genre.dict(by_alias=True))
