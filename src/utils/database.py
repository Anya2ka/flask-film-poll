from pymongo import MongoClient

from ..settings import DATABASE

client = MongoClient(DATABASE.get('HOST'), DATABASE.get('PORT'))
database = client[DATABASE.get('NAME')]
