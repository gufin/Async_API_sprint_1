from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

import core.constants as constants
from api.v1.models import FilmAPI, FilmList
from api.v1.utils import common_parameters
from services.film import BaseService, get_film_service

router = APIRouter()


@router.get(
    "/search",
    response_model=list[FilmList],
    summary=constants.FILM_SEARCH_LIST_SUMMARY,
    description=constants.FILM_SEARCH_LIST_DESCRIPTION,
)
async def film_search_list(
    commons: dict = Depends(common_parameters),
    film_service: BaseService = Depends(get_film_service),
) -> list[FilmList]:
    sort_val = "" if commons["sort"] == "" else commons["sort"].value
    films = await film_service.get_list(
        page_size=commons["page_size"],
        page=commons["page"],
        sort=sort_val,
        genre=commons["genre"],
        query=commons["query"],
        url=commons["request"].url._url,
    )
    return [FilmList.parse_obj(film.dict(by_alias=True)) for film in films]


@router.get(
    "/{film_id}",
    response_model=FilmAPI,
    summary=constants.FILM_ID_SUMMARY,
    description=constants.FILM_ID_DESCRIPTION,
)
async def film_details(
    film_id: str, film_service: BaseService = Depends(get_film_service)
) -> FilmAPI:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=constants.FILM_NOT_FOUND
        )
    return FilmAPI.parse_obj(film.dict(by_alias=True))


@router.get(
    "/",
    response_model=list[FilmList],
    summary=constants.FILM_LIST_SUMMARY,
    description=constants.FILM_LIST_DESCRIPTION,
)
async def film_list(
    commons: dict = Depends(common_parameters),
    film_service: BaseService = Depends(get_film_service),
) -> list[FilmList]:
    sort_val = "" if commons["sort"] == "" else commons["sort"].value
    films = await film_service.get_list(
        page_size=commons["page_size"],
        page=commons["page"],
        sort=sort_val,
        genre=commons["genre"],
        query=commons["query"],
        url=commons["request"].url._url,
    )
    return [FilmList.parse_obj(film.dict(by_alias=True)) for film in films]
