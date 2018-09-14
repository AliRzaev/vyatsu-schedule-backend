from typing import Any, Optional
from unittest import TestCase
from utils.cache import KeyValueStorage, CollectionAdapter, Item


class DummyCollectionAdapter(CollectionAdapter):

    def __init__(self):
        self.dict_ = dict()

    def find_one(self, key: str) -> Optional[Item]:
        document = self.dict_.get(key, None)

        if document is None:
            return None
        else:
            return Item(key, document)

    def update_one(self, key: str, value: Any):
        self.dict_[key] = value

    def delete_one(self, key: str):
        self.dict_.pop(key, None)


class TestKeyValueStorage(TestCase):

    def test_get_value_exist(self):
        adapter = DummyCollectionAdapter()
        adapter.update_one('one', 1)
        storage = KeyValueStorage(adapter)

        value = storage['one']

        self.assertEqual(value, 1, 'Value must be equal to 1')

    def test_get_value_not_exist(self):
        adapter = DummyCollectionAdapter()
        storage = KeyValueStorage(adapter)

        with self.assertRaises(KeyError, msg='It has to raise KeyError exception if there is no such key in storage'):
            value = storage['one']

    def test_set_new_value(self):
        adapter = DummyCollectionAdapter()
        storage = KeyValueStorage(adapter)

        storage['one'] = 1

        value = adapter.dict_.get('one', None)
        self.assertNotEqual(value, None, 'Value must be defined')
        self.assertEqual(value, 1, 'Value must be equal to 1')

    def test_update_value(self):
        adapter = DummyCollectionAdapter()
        adapter.update_one('one', 1)
        storage = KeyValueStorage(adapter)

        storage['one'] = 2

        value = adapter.dict_.get('one', None)
        self.assertNotEqual(value, None, 'Value must be defined')
        self.assertEqual(value, 2, 'Value must be equal to 2')

    def test_delete_value_exist(self):
        adapter = DummyCollectionAdapter()
        adapter.update_one('one', 1)
        storage = KeyValueStorage(adapter)

        del storage['one']

        value = adapter.dict_.get('one', None)
        self.assertEqual(value, None, 'Value must not be defined')

    def test_delete_value_not_exist(self):
        adapter = DummyCollectionAdapter()
        storage = KeyValueStorage(adapter)

        del storage['one']

        value = adapter.dict_.get('one', None)
        self.assertEqual(value, None, 'Value must not be defined')
