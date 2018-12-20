from unittest import TestCase
from pickle import dumps, loads
from time import sleep
from datetime import timedelta

from utils.cache import MongoCollectionAdapter, RedisCollectionAdapter
from utils.mongodb_config import get_collection
from utils.redis_config import get_instance


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


class TestRedisCollectionAdapter(TestCase):

    def clear_all(self):
        self.redis.flushall()

    def setUp(self):
        self.redis = get_instance()
        self.key = 'test_key'
        self.value = dumps('test_value')

    def tearDown(self):
        self.clear_all()

    def test_find_one_if_exists(self):
        self.clear_all()
        self.redis.set(self.key, self.value)
        adapter = RedisCollectionAdapter(self.redis)

        item = adapter.find_one(self.key)

        self.assertIsNotNone(item, 'Item does not exist')
        self.assertEqual(item.key, 'test_key', "Key must be 'test_key'")
        self.assertEqual(item.value, 'test_value', "Value must be 'test_value'")

    def test_find_one_if_doesnt_exists(self):
        self.clear_all()
        adapter = RedisCollectionAdapter(self.redis)

        item = adapter.find_one(self.key)

        self.assertIsNone(item, 'Item exists')

    def test_update_one_expired(self):
        self.clear_all()
        adapter = RedisCollectionAdapter(self.redis, timedelta(seconds=5))

        adapter.update_one(self.key, self.value)
        sleep(6)

        item = adapter.find_one(self.key)
        self.assertIsNone(item, 'Item must be expired')

    def test_update_one_not_expired(self):
        self.clear_all()
        adapter = RedisCollectionAdapter(self.redis, timedelta(seconds=5))

        adapter.update_one(self.key, self.value)
        sleep(2)

        item = adapter.find_one(self.key)
        self.assertIsNotNone(item, 'Item must not be expired')

    def test_update_one_if_exists(self):
        self.clear_all()
        self.redis.set(self.key, self.value)
        adapter = RedisCollectionAdapter(self.redis)

        adapter.update_one(self.key, 'new_value')

        value = loads(self.redis.get(self.key))

        self.assertIsNotNone(value, 'Value does not exist')
        self.assertEqual(value, 'new_value', "Value must be 'new_value'")

    def test_update_one_if_doesnt_exists(self):
        self.clear_all()
        adapter = RedisCollectionAdapter(self.redis)

        adapter.update_one(self.key, 'new_value')

        value = loads(self.redis.get(self.key))

        self.assertIsNotNone(value, 'Value does not exist')
        self.assertEqual(value, 'new_value', "Value must be 'new_value'")

    def test_delete_one_if_exists(self):
        self.clear_all()
        self.redis.set(self.key, self.value)
        adapter = RedisCollectionAdapter(self.redis)

        adapter.delete_one(self.key)

        value = self.redis.get(self.key)

        self.assertIsNone(value, 'Value exists')

    def test_delete_one_if_doesnt_exists(self):
        self.clear_all()
        adapter = RedisCollectionAdapter(self.redis)

        adapter.delete_one(self.key)

        value = self.redis.get(self.key)

        self.assertIsNone(value, 'Value exists')
