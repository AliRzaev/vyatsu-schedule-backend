from typing import Any, Optional
from collections import namedtuple

from pymongo.collection import Collection as MongoCollection


Item = namedtuple('Item', ['key', 'value'])


class CollectionAdapter:

    def find_one(self, key: str) -> Optional[Item]:
        pass

    def update_one(self, key: str, value: Any):
        pass

    def delete_one(self, key: str):
        pass


class MongoCollectionAdapter(CollectionAdapter):
    """
    A collection adapter that uses MongoDB collection as a storage.

    Document scheme:
    {
      'key': string,
      'value': any
    }
    """

    def __init__(self, collection: MongoCollection):
        self._collection = collection

    def find_one(self, key: str) -> Optional[Item]:
        document = self._collection.find_one({
            'key': key
        })

        if document is None:
            return None
        else:
            return Item(document['key'], document['value'])

    def update_one(self, key: str, value: Any):
        self._collection.update_one(
            filter={'key': key},
            update={'$set': {'key': key, 'value': value}},
            upsert=True
        )

    def delete_one(self, key: str):
        self._collection.delete_one({
            'key': key
        })


class KeyValueStorage:
    """
    Simple key-value storage that can use various backends for storing items.
    """

    def __init__(self, collection: CollectionAdapter):
        self._collection = collection

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        document = self._collection.find_one(key)

        if document is None:
            raise KeyError(key)
        else:
            return document.value

    def __setitem__(self, key: str, value: Any):
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        self._collection.update_one(key, value)

    def __delitem__(self, key: str):
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        self._collection.delete_one(key)
