from pymongo import MongoClient
from pymongo.database import Database, Collection
from os import getenv


MONGODB_URI = getenv('MONGODB_URI')

_client = MongoClient(MONGODB_URI)
_database = _client.get_database()


def get_database() -> Database:
    """
    Return database specified in MongoDB URI.
    """
    return _database


def get_collection(name: str) -> Collection:
    """
    Return collection with given name.
    """
    return _database.get_collection(name)
