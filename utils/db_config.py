from pymongo import MongoClient
from pymongo.database import Database, Collection
from os import getenv


MONGODB_URI = getenv('MONGODB_URI')

_client = MongoClient(MONGODB_URI)
_database = _client.get_database()


def get_database() -> Database:
    """
    Get database specified in MongoDB URI
    :return: Database instance
    """
    return _database


def get_collection(collection_name: str) -> Collection:
    """
    Get collection with given name
    :param collection_name:
    :return: Collection instance
    """
    return _database.get_collection(collection_name)
