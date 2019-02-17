from json import load, loads
from logging import disable
from unittest import TestCase

from config.redis import redis_store
from server import app
from utils.prefetch import prefetch


class TestApiV1Groups(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def setUp(self):
        disable()

        self.app = app.test_client()
        self.app.testing = True

        with open('tests/resources/html/groups_info_page.html',
                  'r', encoding='utf-8') as file:
            self.page = file.read()
        with open('tests/resources/v1/test_groups_list.json',
                  'r', encoding='utf-8') as file:
            self.groups_list = load(file)
        with open('tests/resources/v1/test_groups_by_faculty.json',
                  'r', encoding='utf-8') as file:
            self.groups_by_faculty = load(file)

        redis_store.flushdb()

    def test_groups_list(self):
        prefetch(html=self.page)

        response = self.app.get('/api/v1/groups/list')
        actual = loads(response.data)
        expected = self.groups_list

        self.assertEqual(actual, expected, 'Invalid data')

    def test_groups_by_faculty(self):
        prefetch(html=self.page)

        response = self.app.get('/api/v1/groups/by_faculty')
        actual = loads(response.data)
        expected = self.groups_by_faculty

        self.assertEqual(actual, expected, 'Invalid data')


class TestApiV1Calls(TestCase):

    def setUp(self):
        disable()

        self.app = app.test_client()
        self.app.testing = True

        with open('tests/resources/v1/test_calls.json',
                  'r', encoding='utf-8') as file:
            self.calls = load(file)

    def test_calls(self):
        response = self.app.get('/api/v1/calls')
        actual = loads(response.data)
        expected = self.calls

        self.assertEqual(actual, expected, 'Invalid data')
