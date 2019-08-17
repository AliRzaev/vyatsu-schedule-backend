import unittest
from json import load

import responses

from config import TestingConfig
from server import create_app
from utils import prefetch
from utils.extractors import GroupInfo, DepartmentInfo
from utils.repository import get_repository
from utils.university import GROUPS_INFO_URL, DEPARTMENTS_INFO_URL


class TestPrefetch(unittest.TestCase):
    def setUp(self):
        with open('tests/resources/html/groups_info_page.html',
                  'r', encoding='utf-8') as file:
            self.groups_info_page = file.read()

        with open('tests/resources/groups_info.json',
                  'r', encoding='utf-8') as file:
            self.groups_info = sorted(
                (GroupInfo(item['groupId'], item['group'], item['faculty'])
                 for item in load(file)))

        with open('tests/resources/html/departments_info_page.html',
                  'r', encoding='utf-8') as file:
            self.departments_info_page = file.read()

        with open('tests/resources/departments_info.json',
                  'r', encoding='utf-8') as file:
            self.departments_info = sorted(
                (DepartmentInfo(item['departmentId'], item['department'], item['faculty'])
                 for item in load(file)))

    @responses.activate
    def test_prefetch_command(self):
        responses.add(responses.GET, GROUPS_INFO_URL, self.groups_info_page,
                      content_type='text/html; charset=utf8')
        responses.add(responses.GET, DEPARTMENTS_INFO_URL, self.departments_info_page,
                      content_type='text/html; charset=utf8')

        app = create_app(TestingConfig())
        with app.app_context():
            get_repository().drop_all()
        runner = app.test_cli_runner()

        result = runner.invoke(args=['prefetch', '--force'])
        self.assertEqual(result.exit_code, 0)
        self.assertIsNone(result.exception)

        with app.app_context():
            groups = get_repository().get_groups()
            departments = get_repository().get_departments()

            self.assertEqual(sorted(groups), self.groups_info)
            self.assertEqual(sorted(departments), self.departments_info)

    @responses.activate
    def test_prefetch(self):
        responses.add(responses.GET, GROUPS_INFO_URL, self.groups_info_page,
                      content_type='text/html; charset=utf8')
        responses.add(responses.GET, DEPARTMENTS_INFO_URL, self.departments_info_page,
                      content_type='text/html; charset=utf8')

        app = create_app(TestingConfig())
        with app.app_context():
            get_repository().drop_all()

            prefetch.prefetch()

            groups = get_repository().get_groups()
            departments = get_repository().get_departments()

            self.assertEqual(sorted(groups), self.groups_info)
            self.assertEqual(sorted(departments), self.departments_info)
