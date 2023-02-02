from http import HTTPStatus

import core.constants as constants
from api.v1.models import GenreAPI
from api.v1.utils import common_parameters
from fastapi import APIRouter, Depends, HTTPException
from services.genre import BaseService, get_genre_service

router = APIRouter()


@router.get(
    "/search",
    response_model=list[GenreAPI],
    summary=constants.GENRE_SEARCH_LIST_SUMMARY,
    description=constants.GENRE_SEARCH_LIST_DESCRIPTION,
)
async def genre_list_search(
    commons: dict = Depends(common_parameters),
    get_genre_service: BaseService = Depends(get_genre_service),
) -> list[GenreAPI]:
    genres = await get_genre_service.get_list(
        page_size=commons["page_size"],
        page=commons["page"],
        sort=commons["sort"],
        genre=commons["genre"],
        query=commons["query"],
        url=commons["request"].url._url,
    )
    return [GenreAPI.parse_obj(genre.dict(by_alias=True)) for genre in genres]


@router.get(
    "/",
    response_model=list[GenreAPI],
    summary=constants.GENRE_LIST_SUMMARY,
    description=constants.GENRE_LIST_DESCRIPTION,
)
async def genre_list(
    commons: dict = Depends(common_parameters),
    get_genre_service: BaseService = Depends(get_genre_service),
) -> list[GenreAPI]:
    genres = await get_genre_service.get_list(
        page_size=commons["page_size"],
        page=commons["page"],
        sort=commons["sort"],
        genre=commons["genre"],
        query=commons["query"],
        url=commons["request"].url._url,
    )
    return [GenreAPI.parse_obj(genre.dict(by_alias=True)) for genre in genres]


@router.get(
    "/{genre_id}",
    response_model=GenreAPI,
    summary=constants.GENRE_ID_SUMMARY,
    description=constants.GENRE_ID_DESCRIPTION,
)
async def genre_details(
    genre_id: str, genre_service: BaseService = Depends(get_genre_service)
) -> GenreAPI:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=constants.GENRE_NOT_FOUND
        )

    return GenreAPI.parse_obj(genre.dict(by_alias=True))
