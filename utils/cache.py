from typing import Any

from pymongo.collection import Collection as MongoCollection


class CollectionAdapter:

    def find_one(self, key: str) -> Any:
        pass

    def update_one(self, key: str, value: Any):
        pass

    def delete_one(self, key: str):
        pass


class MongoCollectionAdapter(CollectionAdapter):

    def __init__(self, collection: MongoCollection):
        self._collection = collection

    def find_one(self, key: str) -> Any:
        return self._collection.find_one({
            'key': key
        })

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

    def __init__(self, collection: CollectionAdapter):
        self._collection = collection

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        document = self._collection.find_one(key)

        if document is None:
            raise KeyError(key)
        else:
            return document['value']

    def __setitem__(self, key: str, value: Any):
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        self._collection.update_one(key, value)

    def __delitem__(self, key: str):
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        self._collection.delete_one(key)
