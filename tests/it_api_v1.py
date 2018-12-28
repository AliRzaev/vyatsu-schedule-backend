import responses

from json import load, loads
from unittest import TestCase

from server import app
from utils.groups_info import GROUPS_INFO_URL, _get_page


class TestApiV1Groups(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production
    """

    def setUp(self):
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

    def tearDown(self):
        self.clear_cache()

    @staticmethod
    def clear_cache():
        _get_page.cache_clear()

    @responses.activate
    def test_groups_list(self):
        self.clear_cache()
        responses.add(responses.GET, GROUPS_INFO_URL, self.page,
                      content_type='text/html; charset=utf8')

        response = self.app.get('/api/v1/groups/list')
        actual = loads(response.data)
        expected = self.groups_list

        self.assertEqual(actual, expected, 'Invalid data')

    @responses.activate
    def test_groups_by_faculty(self):
        self.clear_cache()
        responses.add(responses.GET, GROUPS_INFO_URL, self.page,
                      content_type='text/html; charset=utf8')

        response = self.app.get('/api/v1/groups/by_faculty')
        actual = loads(response.data)
        expected = self.groups_by_faculty

        self.assertEqual(actual, expected, 'Invalid data')


class TestApiV1Calls(TestCase):

    def setUp(self):
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
