# Important things

- If you want to start application without docker, you should download and install [MongoDB](https://www.mongodb.com/download-center/community)
- For installing dependecies, you should use `pip install -r requirements.txt`
- For starting application without docker, you should use next commands:

```bash
export FLASK_APP=main.py
flask run --host=0.0.0.0 --port=8000
```

- For starting application in development mode without docker, you should use next commands:

```bash
export FLASK_APP=main.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8000
```

- For building docker container, you should use next command:

```bash
docker-compose build
```

- For starting docker containers, you should use next command:

```bash
docker-compose up
```

- For running docker application container (without starting), you should use next command:

```bash
docker-compose run --rm flask-backend bash
```

- For getting database host/port/name, you should use os.getenv(). For example, `db_host = os.getenv('DATABASE_HOST', 'localhost')`
- For creating database client, you should use `MongoClient(db_host, db_port)`. For example, `client = MongoClient(db_host, db_port)`
- For getting access to database, you should use `client[db_name]`. For example, `db = client[db_name]`
- For getting access to database data, you're able to import database from utils and use database client. For example,

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
    'genres': ['cartoon', 'comedy'],
    'votes': []
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
    '_id': bson.objectid.ObjectId('5d2e0934e5a86af54dd42b2e')
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

### Add vote into votes field

```python
import bson
from datetime import datetime
database.movies.update_one(
    {'_id': bson.objectid.ObjectId('5d2e0934e5a86af54dd42b2d')},
    {
        '$push': {
            'votes': {
                'userId': None,
                'value': 8,
                'votedAt': datetime.utcnow()
            }
        }
    }
)
```

### Remove vote from votes field

```python
import bson
database.movies.update_one(
    {'_id': bson.objectid.ObjectId('5d2e0934e5a86af54dd42b2d')},
    {
        '$pull': {
            'votes': {
                'userId': None,
            }
        }
    }
)
```

## Database structure

```json
{
  "Movies": [
    {
      "_id": "<id>",
      "title": "<str>",
      "genres": ["<str>"],
      "votes": [
        {
          "userId": null,
          "value": 5,
          "votedAt": "<date>"
        }
      ]
    }
  ]
}
```
