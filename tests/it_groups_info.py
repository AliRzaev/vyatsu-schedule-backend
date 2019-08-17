from json import load
from unittest import TestCase

from config import TestingConfig
from server import create_app
from utils.extractors import *
from utils.repository import get_repository


def _create_app():
    return create_app(TestingConfig())


class TestGroupsInfo(TestCase):
    """
    Be attentive! This test case may wipe out data in your database.
    Please ensure that you run test case with database for testing,
    not for production.
    """

    def setUp(self):
        with open('tests/resources/html/groups_info_page.html',
                  'r', encoding='utf-8') as file:
            self.page = file.read()

        with open('tests/resources/groups_info.json',
                  'r', encoding='utf-8') as file:
            self.info = sorted(
                (GroupInfo(item['groupId'], item['group'], item['faculty'])
                 for item in load(file)))

    def _prefetch(self):
        groups = extract_groups(self.page)
        groups_date_ranges = extract_date_ranges(self.page)

        get_repository().update_groups_info(groups, groups_date_ranges, True)

    def test_get_groups(self):
        app = _create_app()
        with app.app_context():
            self._prefetch()

            actual = sorted(get_repository().get_groups())
            expected = self.info

            self.assertEqual(actual, expected)
