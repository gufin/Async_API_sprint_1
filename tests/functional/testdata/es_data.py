import uuid

low_rating = [
    {
        "id": str(uuid.uuid4()),
        "imdb_rating": 3.5,
        "genres": [
            {"id": str(uuid.uuid4()), "name": "Action"},
            {"id": str(uuid.uuid4()), "name": "Sci-Fi"},
        ],
        "title": "Low rating title",
        "description": "My test description",
        "directors_names": ["Madikhan", 'Bob'],
        "actors_names": ["Jonh", "Kavic"],
        "writers_names": ["Mick", "Potter"],
        "directors": [
            {"id": str(uuid.uuid4()), "full_name": "Dany"},
        ],
        "actors": [
            {"id": str(uuid.uuid4()), "full_name": "Margarit"},
            {"id": str(uuid.uuid4()), "full_name": "Katrin"},
        ],
        "writers": [
            {"id": str(uuid.uuid4()), "full_name": "Jonh"},
            {"id": str(uuid.uuid4()), "full_name": "Madikhan"},
        ],
    }
]

high_rating = [
    {
        "id": str(uuid.uuid4()),
        "imdb_rating": 9.3,
        "genres": [
            {"id": str(uuid.uuid4()), "name": "Action"},
            {"id": str(uuid.uuid4()), "name": "Sci-Fi"},
        ],
        "title": "High rating title",
        "description": "My test description",
        "directors_names": ["Madikhan", 'Bob'],
        "actors_names": ["Jonh", "Kavic"],
        "writers_names": ["Mick", "Potter"],
        "directors": [
            {"id": str(uuid.uuid4()), "full_name": "Dany"},
        ],
        "actors": [
            {"id": str(uuid.uuid4()), "full_name": "Margarit"},
            {"id": str(uuid.uuid4()), "full_name": "Katrin"},
        ],
        "writers": [
            {"id": str(uuid.uuid4()), "full_name": "Jonh"},
            {"id": str(uuid.uuid4()), "full_name": "Madikhan"},
        ],
    }
]

film_work_data = (
    [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 6.6,
            "genres": [
                {"id": str(uuid.uuid4()), "name": "Action"},
                {"id": str(uuid.uuid4()), "name": "Sci-Fi"},
            ],
            "title": f"film π{i}",
            "description": "My test description",
            "directors_names": ["Madikhan", 'Bob'],
            "actors_names": ["Jonh", "Kavic"],
            "writers_names": ["Mick", "Potter"],
            "directors": [
                {"id": str(uuid.uuid4()), "full_name": "Dany"},
            ],
            "actors": [
                {"id": str(uuid.uuid4()), "full_name": "Margarit"},
                {"id": str(uuid.uuid4()), "full_name": "Katrin"},
            ],
            "writers": [
                {"id": str(uuid.uuid4()), "full_name": "Jonh"},
                {"id": str(uuid.uuid4()), "full_name": "Madikhan"},
            ],
        }
        for i in range(20)
    ]
    + low_rating
    + high_rating
)

genres_data = [
    {"id": str(uuid.uuid4()), "name": "Action", "description": "Action movies"}
    for _ in range(20)
] + [
    {
        "id": str(uuid.uuid4()),
        "name": "Thriller",
        "description": "Scary movies",
    }
    for _ in range(20)
]

persons_data = [
    {
        "id": str(uuid.uuid4()),
        "full_name": "Peter Cushing",
        "films": {
            "actor": [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Lego Star Wars: The Complete Saga",
                    "imdb_rating": 8.5,
                },
            ],
        },
    }
    for _ in range(20)
]
