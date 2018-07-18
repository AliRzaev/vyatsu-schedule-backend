from typing import Any

from pymongo.collection import Collection


class KeyValueStorage:

    def __init__(self, collection: Collection):
        self._collection = collection

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        document = self._collection.find_one({
            'key': key
        })

        if document is None:
            raise KeyError(key)
        else:
            return document['value']

    def __setitem__(self, key: str, value: Any):
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        self._collection.update_one(
            filter={'key': key},
            update={'$set': {'key': key, 'value': value}},
            upsert=True
        )

    def __delitem__(self, key: str):
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        self._collection.delete_one({
            'key': key
        })
