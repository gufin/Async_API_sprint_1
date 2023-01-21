from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from api.v1.models import GenreAPI
from services.genre import BaseService, get_genre_service

router = APIRouter()


@router.get('/',
            response_model=list[GenreAPI],
            summary='Shows a list of genres',
            description='Shows a list of genres'
            )
async def genre_list(
        request: Request,
        page_size: int = Query(10, description='Number of films on page'),
        page: int = Query(1, description='Page number'),
        sort: str = Query('',
                          description='Sorting field. '
                                      'Example: imdb_rating:desc'),
        genre: str = Query(None, description='Filter by genre uuid'),
        get_genre_service: BaseService = Depends(get_genre_service)
) -> list[GenreAPI]:
    genres = await get_genre_service.get_list(page_size=page_size,
                                              page=page,
                                              sort=sort,
                                              genre=genre,
                                              url=request.url._url, )
    return [GenreAPI.parse_obj(genre.dict(by_alias=True)) for genre in
            genres]


@router.get('/{genre_id}',
            response_model=GenreAPI,
            summary='Shows detailed information about the genre',
            description='Shows detailed information about the genre'
            )
async def genre_details(genre_id: str,
                        genre_service: BaseService = Depends(
                            get_genre_service)
                        ) -> GenreAPI:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='genre not found')

    return GenreAPI.parse_obj(genre.dict(by_alias=True))
