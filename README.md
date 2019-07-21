# Important things

-   If you want to start application without docker, you should download and install [MongoDB](https://www.mongodb.com/download-center/community)
-   For installing dependecies, you should use `pip install -r requirements.txt`
-   For starting application without docker, you should use next commands:

```bash
export FLASK_APP=main.py
flask run --host=0.0.0.0 --port=8000
```

-   For starting application in development mode without docker, you should use next commands:

```bash
export FLASK_APP=main.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8000
```

-   For building docker container, you should use next command:

```bash
docker-compose build
```

-   For starting docker containers, you should use next command:

```bash
docker-compose up
```

-   For running docker application container (without starting), you should use next command:

```bash
docker-compose run --rm flask-backend bash
```

-   For getting database host/port/name, you should use os.getenv(). For example, `db_host = os.getenv('DATABASE_HOST', 'localhost')`
-   For creating database client, you should use `MongoClient(db_host, db_port)`. For example, `client = MongoClient(db_host, db_port)`
-   For getting access to database, you should use `client[db_name]`. For example, `db = client[db_name]`
-   For getting access to database data, you're able to import database from utils and use database client. For example,

```
>>> from src.utils.database import database
>>> database.users.find()
<pymongo.cursor.Cursor object at 0x7f6f0ccf0f60>
>>> for user in database.users.find():
...   print(user)
...
>>> database.users.insert_one({'firstName': 'Ann', 'lastName': 'Basova'})
<pymongo.results.InsertOneResult object at 0x7f6f0cd08248>
>>> for user in database.users.find():
...   print(user)
...
{'lastName': 'Basova', 'firstName': 'Ann', '_id': ObjectId('5d2b7b38269409bedd14604f')}
>>> database.users.drop()
>>> for user in database.users.find():
...   print(user)
...
>>>
```

## Working with MongoDB (PyMongo)

### Create movie in collection

```python
database.movies.insert_one({
    'title': 'Zootopia',
    'genres': ['cartoon', 'comedy']
})
```

### Update movie in collection

```python
import bson
database.movies.update_one(
    {'_id': bson.objectid.ObjectId('5d2e0934e5a86af54dd42b2d')},
    {'$set': {'title': '1 + 1'}}
)
```

### Delete movie from collection

```python
import bson
database.movies.delete_one({
    '_id': bson.objectid.ObjectId('5d3302d443cdef124736ae25')
})
```

### Get all movies from collection

```python
database.movies.find()
```

### Get movie by id

```python
import bson

database.movies.find_one({
    '_id': bson.objectid.ObjectId('5d2e0934e5a86af54dd42b2d')
})
```

## Database structure

```json
{
    "Movies": [
        {
            "_id": "<id>",
            "title": "<str>",
            "genres": ["<str>"]
        }
    ],
    "Polls": [
        {
            "_id": "<id>",
            "movies": {
                "<id>": [
                    {
                        "value": 0,
                        "votedAt": "<date>"
                    }
                ]
            }
        }
    ]
}
```

## Project structure

```
<project-name>
    .git
    .gitignore
    Dockerfile
    docker-compose.yml
    README.md
    requirements.txt
    main.py

    src
        __init__.py
        settings.py

        views
            __init__.py
            movies.py
            polls.py

        services
            __init__.py
            movies.py
            polls.py

        utils
            __init__.py
            database.py
```

## Endpoints

| Method | Endpoint                | Data                                      | Description                                |
| ------ | ----------------------- | ----------------------------------------- | ------------------------------------------ |
| GET    | `/movies/`              |                                           | Get list of movies                         |
| POST   | `/movies/`              | `{"title": "<str>", "genres": ["<str>"]}` | Create movie                               |
| GET    | `/movies/<id>/`         |                                           | Fetch movie details by id                  |
| PATCH  | `/movies/<id>/`         | `{"title": "<str>", "genres": ["<str>"]}` | Update movie by id                         |
| DELETE | `/movies/<id>/`         |                                           | Delete movie by id                         |
| POST   | `/polls/`               | `{"movies": {"<id>": 0}}`                 | Create a new poll                          |
| GET    | `/polls/`               |                                           | Fetch list of polls                        |
| GET    | `/polls/<id>/`          |                                           | Fetch poll details by id                   |
| PATCH  | `/polls/<id>/`          | `{"movies": {"<id>": 0}}`                 | Update poll by id                          |
| DELETE | `/polls/<id>/`          |                                           | Delete poll by id                          |
| PUT    | `/polls/<id>/<movieId>` | `{"value": 0}`                            | Update movie results by PollID and MovieID |
