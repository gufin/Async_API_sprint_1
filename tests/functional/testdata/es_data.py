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
        "id": '4a6ab249-1a59-4207-86c8-7e72023d268e',
        "imdb_rating": 9.3,
        "genres": [
            {"id": "d6673ce4-f6f5-4050-8723-86ed289d950b", "name": "Action"},
            {"id": "b09f9f5d-9d98-47a5-9762-484456857c96", "name": "Sci-Fi"},
        ],
        "title": "High rating title",
        "description": "My test description",
        "directors_names": ["Madikhan", 'Bob'],
        "actors_names": ["Jonh", "Kavic"],
        "writers_names": ["Mick", "Potter"],
        "directors": [
            {"id": "7fe82bc5-ce75-44e7-b6dc-b3e6abe62309", "full_name": "Dany"},
        ],
        "actors": [
            {"id": "66de8179-783e-47a8-8053-effcfd7636de", "full_name": "Margarit"},
            {"id": "fb40ac45-6929-4b61-a0d5-261e0dff328b", "full_name": "Katrin"},
        ],
        "writers": [
            {"id": "b817767c-f4c4-4042-b0a4-7ce207223349", "full_name": "Jonh"},
            {"id": '12dc90d2-3806-42ae-8bd7-44029b4c092d', "full_name": "Madikhan"},
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
            "title": f"film №{i}",
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
        "id": "0ee5e6ef-2cd0-49db-8f71-8030f590d220",
        "name": "Thriller",
        "description": "Scary movies",
    }
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
] + [
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "full_name": "Madikhan Agatanov",
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
