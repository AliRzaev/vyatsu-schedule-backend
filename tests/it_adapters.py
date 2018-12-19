from unittest import TestCase

from utils.cache import MongoCollectionAdapter
from utils.mongodb_config import get_collection


class TestMongoCollectionAdapter(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production
    """

    def clear_collection(self):
        self.collection.delete_many(dict())

    def setUp(self):
        self.collection = get_collection('test_collection')
        self.document = {
            'key': 'test_key',
            'value': 'test_value'
        }

    def tearDown(self):
        self.clear_collection()

    def test_find_one_if_exists(self):
        self.clear_collection()
        self.collection.insert_one(self.document)
        adapter = MongoCollectionAdapter(self.collection)

        item = adapter.find_one('test_key')

        self.assertIsNotNone(item, 'Item does not exist')
        self.assertEqual(item.key, 'test_key', "Key must be 'test_key'")
        self.assertEqual(item.value, 'test_value', "Value must be 'test_value'")

    def test_find_one_if_doesnt_exists(self):
        self.clear_collection()
        adapter = MongoCollectionAdapter(self.collection)

        item = adapter.find_one('test_key')

        self.assertIsNone(item, 'Item exists')

    def test_update_one_if_exists(self):
        self.clear_collection()
        self.collection.insert_one(self.document)
        adapter = MongoCollectionAdapter(self.collection)

        adapter.update_one('test_key', 'new_value')

        document = self.collection.find_one({'key': 'test_key'})

        self.assertIsNotNone(document, 'Document does not exist')
        self.assertEqual(document['value'], 'new_value', "Value must be 'new_value'")

    def test_update_one_if_doesnt_exists(self):
        self.clear_collection()
        adapter = MongoCollectionAdapter(self.collection)

        adapter.update_one('test_key', 'new_value')

        document = self.collection.find_one({'key': 'test_key'})

        self.assertIsNotNone(document, 'Document does not exist')
        self.assertEqual(document['value'], 'new_value', "Value must be 'new_value'")

    def test_delete_one_if_exists(self):
        self.clear_collection()
        self.collection.insert_one(self.document)
        adapter = MongoCollectionAdapter(self.collection)

        adapter.delete_one('test_key')

        document = self.collection.find_one({'key': 'test_key'})

        self.assertIsNone(document, 'Document exists')

    def test_delete_one_if_doesnt_exists(self):
        self.clear_collection()
        adapter = MongoCollectionAdapter(self.collection)

        adapter.delete_one('test_key')

        document = self.collection.find_one({'key': 'test_key'})

        self.assertIsNone(document, 'Document exists')
