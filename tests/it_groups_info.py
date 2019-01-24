from json import load
from unittest import TestCase

from config.redis import get_instance
from utils.extractors import *
from utils.groups_info import get_groups
from utils.prefetch import prefetch


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

        get_instance().flushdb()

    def test_get_groups(self):
        prefetch(html=self.page)

        actual = sorted(get_groups())
        expected = self.info

        self.assertEqual(actual, expected)
