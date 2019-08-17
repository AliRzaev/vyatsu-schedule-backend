from json import load
from unittest import TestCase

from config import TestingConfig
from server import create_app
from utils.extractors import *
from utils.repository import get_repository


def _create_app():
    return create_app(TestingConfig())


class TestDepartmentsInfo(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def setUp(self):
        with open('tests/resources/html/departments_info_page.html',
                  'r', encoding='utf-8') as file:
            self.page = file.read()

        with open('tests/resources/departments_info.json',
                  'r', encoding='utf-8') as file:
            self.info = sorted(
                (DepartmentInfo(item['departmentId'], item['department'], item['faculty'])
                 for item in load(file)))

    def _prefetch(self):
        departments = extract_departments(self.page)
        departments_date_ranges = extract_departments_date_ranges(self.page)

        get_repository().update_departments_info(
            departments, departments_date_ranges, True
        )

    def test_get_departments(self):
        app = _create_app()
        with app.app_context():
            self._prefetch()

            actual = sorted(get_repository().get_departments())
            expected = self.info

            self.assertEqual(actual, expected)
