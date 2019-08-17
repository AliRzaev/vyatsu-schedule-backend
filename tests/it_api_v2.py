from json import load, loads
from unittest import TestCase

from loguru import logger

from config import TestingConfig
from server import create_app
from utils.extractors import extract_groups, extract_date_ranges, extract_departments, extract_departments_date_ranges
from utils.repository import get_repository


def _create_app():
    return create_app(TestingConfig())


class TestApiV2Groups(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def setUp(self):
        logger.disable('server')

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

    def _prefetch(self):
        groups = extract_groups(self.page)
        groups_date_ranges = extract_date_ranges(self.page)

        get_repository().update_groups_info(groups, groups_date_ranges, True)

    def test_groups_list(self):
        app = _create_app()
        with app.test_client() as client:
            with app.app_context():
                self._prefetch()

            response = client.get('/api/v2/groups/list')
            actual = loads(response.data)
            expected = self.groups_list

        self.assertEqual(actual, expected, 'Invalid data')

    def test_groups_by_faculty(self):
        app = _create_app()
        with app.test_client() as client:
            with app.app_context():
                self._prefetch()

            response = client.get('/api/v2/groups/by_faculty')
            actual = loads(response.data)
            expected = self.groups_by_faculty

            self.assertEqual(actual, expected, 'Invalid data')


class TestApiV2Departments(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def setUp(self):
        logger.disable('server')

        with open('tests/resources/html/departments_info_page.html',
                  'r', encoding='utf-8') as file:
            self.page = file.read()
        with open('tests/resources/v2/test_departments_list.json',
                  'r', encoding='utf-8') as file:
            self.departments_list = sorted(load(file), key=lambda x: x['name'])
        with open('tests/resources/v2/test_departments_by_faculty.json',
                  'r', encoding='utf-8') as file:
            self.departments_by_faculty = load(file)
            self.departments_by_faculty.sort(key=lambda x: x['faculty'])
            for faculty in self.departments_by_faculty:
                faculty['departments'].sort(key=lambda x: x['name'])

    def _prefetch(self):
        departments = extract_departments(self.page)
        departments_date_ranges = extract_departments_date_ranges(self.page)

        get_repository().update_departments_info(departments, departments_date_ranges, True)

    def test_departments_list(self):
        app = _create_app()
        with app.test_client() as client:
            with app.app_context():
                self._prefetch()

            response = client.get('/api/v2/departments/list')
            actual = loads(response.data)
            expected = self.departments_list

            self.assertEqual(actual, expected, 'Invalid data')

    def test_departments_by_faculty(self):
        app = _create_app()
        with app.test_client() as client:
            with app.app_context():
                self._prefetch()

            response = client.get('/api/v2/departments/by_faculty')
            actual = loads(response.data)
            expected = self.departments_by_faculty

            self.assertEqual(actual, expected, 'Invalid data')


class TestApiV2Calls(TestCase):

    def setUp(self):
        logger.disable('server')

        with open('tests/resources/v2/test_calls.json',
                  'r', encoding='utf-8') as file:
            self.calls = load(file)

    def test_calls(self):
        app = _create_app()
        with app.test_client() as client:
            response = client.get('/api/v2/calls')
            actual = loads(response.data)
            expected = self.calls

            self.assertEqual(actual, expected, 'Invalid data')
