from json import load, loads
from logging import CRITICAL
from unittest import TestCase

import responses

import server
from server import app
from utils.groups_info import GROUPS_INFO_URL, _get_page
from utils.logging import get_logger


class TestApiV2Groups(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def setUp(self):
        get_logger(server.__name__).setLevel(CRITICAL)  # disable logging

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

        response = self.app.get('/api/v2/groups/list')
        actual = loads(response.data)
        expected = self.groups_list

        self.assertEqual(actual, expected, 'Invalid data')

    @responses.activate
    def test_groups_by_faculty(self):
        self.clear_cache()
        responses.add(responses.GET, GROUPS_INFO_URL, self.page,
                      content_type='text/html; charset=utf8')

        response = self.app.get('/api/v2/groups/by_faculty')
        actual = loads(response.data)
        expected = self.groups_by_faculty

        self.assertEqual(actual, expected, 'Invalid data')


class TestApiV2Calls(TestCase):

    def setUp(self):
        get_logger(server.__name__).setLevel(CRITICAL)  # disable logging

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
