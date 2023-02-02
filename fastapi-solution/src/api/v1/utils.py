from core import constants
from fastapi import Query, Request


async def common_parameters(
    request: Request,
    page_size: int = Query(
        10, description=constants.PAGE_SIZE_DESCRIPTION, ge=1
    ),
    page: int = Query(1, description=constants.PAGE_DESCRIPTION, ge=1),
    genre: str = Query(None, description=constants.GENRE_FILTER_DESCRIPTION),
    sort: constants.FilmsSortingFields = Query(
        "", description=constants.SORT_DESCRIPTION
    ),
    query: str = Query(None, description=constants.FILM_SEARCH_DESCRIPTION),
):
    return {
        "request": request,
        "page_size": page_size,
        "page": page,
        "sort": sort,
        "query": query,
        "genre": genre,
    }
