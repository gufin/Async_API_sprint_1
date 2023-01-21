from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from api.v1.models import FilmAPI, FilmList
from services.film import BaseService, get_film_service

router = APIRouter()


@router.get('/{film_id}',
            response_model=FilmAPI,
            summary='Shows detailed information about the movie',
            description=('Shows detailed information about the movie '
                         'such as actors directors scriptwriters description '
                         'and rating'),
            )
async def film_details(film_id: str,
                       film_service: BaseService = Depends(get_film_service)
                       ) -> FilmAPI:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail='film not found')
    return FilmAPI.parse_obj(film.dict(by_alias=True))


@router.get('/',
            response_model=list[FilmList],
            summary='Shows a list of movies',
            description='Shows a list of movies'
            )
async def film_list(
        request: Request,
        page_size: int = Query(10, description='Number of films on page'),
        page: int = Query(1, description='Page number'),
        sort: str = Query('',
                          description='Sorting field. '
                                      'Example: imdb_rating:desc'),
        genre: str = Query(None, description='Filter by genre uuid'),
        film_service: BaseService = Depends(get_film_service)
) -> list[FilmList]:
    films = await film_service.get_list(page_size=page_size,
                                        page=page,
                                        sort=sort,
                                        genre=genre,
                                        url=request.url._url, )
    return [FilmList.parse_obj(film.dict(by_alias=True)) for film in films]
