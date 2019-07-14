# Important things

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
