settings = {
    "index": {
        "refresh_interval": "1s",
        "number_of_shards": "1",
        "analysis": {
            "filter": {
                "russian_stemmer": {"type": "stemmer", "language": "russian"},
                "english_stemmer": {"type": "stemmer", "language": "english"},
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english",
                },
                "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                "english_stop": {"type": "stop", "stopwords": "_english_"},
            },
            "analyzer": {
                "ru_en": {
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer",
                    ],
                    "tokenizer": "standard",
                }
            },
        },
    }
}

MOVIES_INDEX = {
    "index": "movies",
    "body": {
        "settings": settings,
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "imdb_rating": {"type": "float"},
                "genres": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {"type": "keyword"},
                        "name": {"type": "text", "analyzer": "ru_en"},
                    },
                },
                "title": {
                    "type": "text",
                    "analyzer": "ru_en",
                    "fields": {"raw": {"type": "keyword"}},
                },
                "description": {"type": "text", "analyzer": "ru_en"},
                "directors_names": {"type": "text", "analyzer": "ru_en"},
                "actors_names": {"type": "text", "analyzer": "ru_en"},
                "writers_names": {"type": "text", "analyzer": "ru_en"},
                "actors": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {"type": "keyword"},
                        "full_name": {"type": "text", "analyzer": "ru_en"},
                    },
                },
                "directors": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {"type": "keyword"},
                        "full_name": {"type": "text", "analyzer": "ru_en"},
                    },
                },
                "writers": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {"type": "keyword"},
                        "full_name": {"type": "text", "analyzer": "ru_en"},
                    },
                },
            },
        },
    },
}
GENRES_INDEX = {
    "index": "genres",
    "body": {
        "settings": settings,
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "ru_en"},
                "description": {"type": "text", "analyzer": "ru_en"},
            },
        },
    },
}

PERSONS_INDEX = {
    "index": "persons",
    "body": {
        "settings": settings,
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": {"type": "keyword"},
                "full_name": {
                    "type": "text",
                    "analyzer": "ru_en",
                    "fields": {"raw": {"type": "keyword"}},
                },
                "films": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "actor": {
                            "type": "nested",
                            "dynamic": "strict",
                            "properties": {
                                "id": {"type": "keyword"},
                                "imdb_rating": {"type": "float"},
                                "title": {
                                    "type": "text",
                                    "analyzer": "ru_en",
                                    "fields": {"raw": {"type": "keyword"}},
                                },
                            },
                        },
                        "writer": {
                            "type": "nested",
                            "dynamic": "strict",
                            "properties": {
                                "id": {"type": "keyword"},
                                "imdb_rating": {"type": "float"},
                                "title": {
                                    "type": "text",
                                    "analyzer": "ru_en",
                                    "fields": {"raw": {"type": "keyword"}},
                                },
                            },
                        },
                        "director": {
                            "type": "nested",
                            "dynamic": "strict",
                            "properties": {
                                "id": {"type": "keyword"},
                                "imdb_rating": {"type": "float"},
                                "title": {
                                    "type": "text",
                                    "analyzer": "ru_en",
                                    "fields": {"raw": {"type": "keyword"}},
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}
