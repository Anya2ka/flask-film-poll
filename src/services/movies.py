import bson

from ..utils.database import database


def create(data={}):
    return database.movies.insert_one(data).inserted_id


def find(query={}):
    return list(database.movies.find(query))


def find_by_id(movie_id):
    result = database.movies.find_one({
        '_id': bson.objectid.ObjectId(movie_id)
    })

    if result is None:
        raise ValueError("Invalid id")

    return result


def update(movie_id, data={}):
    result = database.movies.update_one(
        {'_id': bson.objectid.ObjectId(movie_id)},
        {'$set': data}
    )

    if result.matched_count == 0:
        raise ValueError("Invalid id")


def delete(movie_id):
    result = database.movies.delete_one({
        '_id': bson.objectid.ObjectId(movie_id)
    })

    if result.deleted_count == 0:
        raise ValueError("Invalid id")
