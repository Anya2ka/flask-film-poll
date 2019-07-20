import bson

from ..utils.database import database


def create(data={}):
    return database.movies.insert_one(data).inserted_id


def find():
    return list(database.movies.find())


def find_by_id(_id):
    result = database.movies.find_one({
        '_id': bson.objectid.ObjectId(_id)
    })

    if result is None:
        raise ValueError("Invalid id")

    return result


def update(_id, data={}):
    result = database.movies.update_one(
        {'_id': bson.objectid.ObjectId(_id)},
        {'$set': data}
    )

    if result.matched_count == 0:
        raise ValueError("Invalid id")

    return _id


def delete(_id):
    result = database.movies.delete_one({
        '_id': bson.objectid.ObjectId(_id)
    })

    if result.deleted_count == 0:
        raise ValueError("Invalid id")

    return _id
