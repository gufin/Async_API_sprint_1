from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from models.models import UUIDMixin
from services.genre import GenreService, get_genre_service

router = APIRouter()


class GenreAPI(UUIDMixin, BaseModel):
    name: str


@router.get('/', response_model=list[GenreAPI])
async def genre_list(
        page_size: int = Query(10, description='Number of films on page'),
        page: int = Query(1, description='Page number'),
        sort: str = Query('',
                          description='Sorting field. '
                                      'Example: imdb_rating:desc'),
        genre: str = Query(None, description='Filter by genre uuid'),
        get_genre_service: GenreService = Depends(get_genre_service)
) -> list[GenreAPI]:
    genres = await get_genre_service.get_list(page_size=page_size,
                                              page=page,
                                              sort=sort,
                                              genre=genre)
    return [GenreAPI.parse_obj(genre.dict(by_alias=True)) for genre in
            genres]


@router.get('/{genre_id}', response_model=GenreAPI)
async def genre_details(genre_id: str,
                        genre_service: GenreService = Depends(
                            get_genre_service)
                        ) -> GenreAPI:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='genre not found')

    genre_api = GenreAPI.parse_obj(genre.dict(by_alias=True))
    return genre_api
