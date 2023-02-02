from enum import Enum

FILM_ID_SUMMARY = "Shows detailed information about the movie"
FILM_ID_DESCRIPTION = (
    "Shows detailed information about the movie "
    "such as actors directors scriptwriters description "
    "and rating"
)
FILM_NOT_FOUND = "film not found"
FILM_LIST_SUMMARY = "Shows a list of movies"
FILM_LIST_DESCRIPTION = "Shows a list of movies"
FILM_SEARCH_LIST_DESCRIPTION = (
    "Shows a list of movies matching the " "search criteria"
)
FILM_SEARCH_LIST_SUMMARY = (
    "Shows a list of movies matching the search criteria"
)
FILM_SEARCH_DESCRIPTION = "Part of the movie title (Example: dark sta )"
GENRE_ID_SUMMARY = "Shows detailed information about the genre"
GENRE_ID_DESCRIPTION = "Shows detailed information about the genre"
GENRE_NOT_FOUND = "genre not found"
GENRE_LIST_SUMMARY = "Shows a list of genres"
GENRE_LIST_DESCRIPTION = "Shows a list of genres"
GENRE_SEARCH_LIST_SUMMARY = (
    "Shows a list of genres matching the search criteria"
)
GENRE_SEARCH_LIST_DESCRIPTION = (
    "Shows a list of genres matching the search criteria"
)
GENRE_SEARCH_DESCRIPTION = "Part of the genre title (Example: horr )"
PERSON_ID_SUMMARY = "Shows detailed information about the person"
PERSON_ID_DESCRIPTION = (
    "Shows detailed information about the person. "
    "In what films did he participate and in what role"
)
PERSON_NOT_FOUND = "person not found"
PERSON_LIST_SUMMARY = "Shows a list of persons"
PERSON_LIST_DESCRIPTION = "Shows a list of persons"
PERSON_SEARCH_LIST_SUMMARY = (
    "Shows a list of persons matching the search criteria"
)
PERSON_SEARCH_LIST_DESCRIPTION = (
    "Shows a list of persons matching the search criteria"
)
PERSON_SEARCH_DESCRIPTION = "Part of the person name (Example: Harrison )"
PERSON_FILMS_SUMMARY = "Shows films in which the person took part"
PERSON_FILMS_DESCRIPTION = "Shows films in which the person took part"
PAGE_SIZE_DESCRIPTION = "Number of films on page"
PAGE_DESCRIPTION = "Page number"
SORT_DESCRIPTION = "Sorting field. Example: imdb_rating:desc"
GENRE_FILTER_DESCRIPTION = "Filter by genre uuid"


class FilmsSortingFields(str, Enum):
    imdb_rating_asc = "imdb_rating:asc"
    imdb_rating_desc = "imdb_rating:desc"
    age_limit_asc = "age_limit"
    age_limit_desc = "age_limit:desc"


class GenreSortingFields(str, Enum):
    name_asc = "name:asc"
    name_desc = "name:desc"
