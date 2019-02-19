from json import load, loads
from logging import disable, CRITICAL
from unittest import TestCase

from config.redis import redis_store
from server import app
from utils.prefetch import prefetch


class TestApiV2Groups(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def setUp(self):
        disable(CRITICAL)

        self.app = app.test_client()
        self.app.testing = True

        with open('tests/resources/html/groups_info_page.html',
                  'r', encoding='utf-8') as file:
            self.page = file.read()
        with open('tests/resources/v2/test_groups_list.json',
                  'r', encoding='utf-8') as file:
            self.groups_list = sorted(load(file), key=lambda x: x['name'])
        with open('tests/resources/v2/test_groups_by_faculty.json',
                  'r', encoding='utf-8') as file:
            self.groups_by_faculty = load(file)
            self.groups_by_faculty.sort(key=lambda x: x['faculty'])
            for faculty in self.groups_by_faculty:
                faculty['groups'].sort(key=lambda x: x['name'])

        redis_store.flushdb()

    def test_groups_list(self):
        prefetch(html=self.page, redis=redis_store)

        response = self.app.get('/api/v2/groups/list')
        actual = loads(response.data)
        expected = self.groups_list

        self.assertEqual(actual, expected, 'Invalid data')

    def test_groups_by_faculty(self):
        prefetch(html=self.page, redis=redis_store)

        response = self.app.get('/api/v2/groups/by_faculty')
        actual = loads(response.data)
        expected = self.groups_by_faculty

        self.assertEqual(actual, expected, 'Invalid data')


class TestApiV2Calls(TestCase):

    def setUp(self):
        disable(CRITICAL)

        self.app = app.test_client()
        self.app.testing = True

        with open('tests/resources/v2/test_calls.json',
                  'r', encoding='utf-8') as file:
            self.calls = load(file)

    def test_calls(self):
        response = self.app.get('/api/v2/calls')
        actual = loads(response.data)
        expected = self.calls

        self.assertEqual(actual, expected, 'Invalid data')
