import bson

from ..utils.database import database
from datetime import datetime


def create(data={}):
    return database.polls.insert_one(data).inserted_id


def find():
    return list(database.polls.find())


def find_by_id(_id):
    result = database.polls.find_one({
        '_id': bson.objectid.ObjectId(_id)
    })

    if result is None:
        raise ValueError("Invalid id")

    return result


def update(_id, data={}):
    result = database.polls.update_one(
        {'_id': bson.objectid.ObjectId(_id)},
        {'$set': data}
    )

    if result.matched_count == 0:
        raise ValueError("Invalid id")


def update_by_details(_id, movie_id, value=None):
    if (
        database.movies.find_one({
            '_id': bson.objectid.ObjectId(movie_id)
        }) is None
    ):
        raise ValueError('Movie with _id \'{}\' not found '.format(movie_id))

    key = 'movies.{}'.format(movie_id)
    data = {'votedAt': datetime.now(), 'value': value}
    result = database.polls.update_one(
        {'_id': bson.objectid.ObjectId(_id)},
        {'$push': {key: data}}
    )

    if result.matched_count == 0:
        raise ValueError('Poll with _id \'{}\' not found '.format(_id))


def delete(_id):
    result = database.polls.delete_one({
        '_id': bson.objectid.ObjectId(_id)
    })

    if result.deleted_count == 0:
        raise ValueError("Invalid id")
