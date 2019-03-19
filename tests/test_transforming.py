from json import load
from unittest import TestCase

from utils.extractors import GroupInfo, DepartmentInfo
from utils.transforming import api_v1, api_v2


class TestTransformingV1(TestCase):

    def setUp(self):
        with open('tests/resources/groups_info.json',
                  'r', encoding='utf-8') as file:
            self.data = tuple(GroupInfo(item['groupId'],
                                        item['group'],
                                        item['faculty']) for item in load(file))

    def test_groups_list(self):
        actual = api_v1.groups_info_to_dict(self.data)

        with open('tests/resources/v1/test_groups_list.json',
                  'r', encoding='utf-8') as file:
            expected = load(file)

        self.assertEqual(actual, expected, 'Invalid transformation')

    def test_groups_by_faculty(self):
        actual = api_v1.groups_info_to_dict(self.data, True)

        with open('tests/resources/v1/test_groups_by_faculty.json',
                  'r', encoding='utf-8') as file:
            expected = load(file)

        self.assertEqual(actual, expected, 'Invalid transformation')


class TestTransformingV2(TestCase):

    def setUp(self):
        with open('tests/resources/groups_info.json',
                  'r', encoding='utf-8') as file:
            self.groups_data = tuple(GroupInfo(item['groupId'],
                                               item['group'],
                                               item['faculty']) for item in
                                     load(file))

        with open('tests/resources/departments_info.json',
                  'r', encoding='utf-8') as file:
            self.departments_data = tuple(DepartmentInfo(
                item['departmentId'],
                item['department'],
                item['faculty']) for item in load(file))

    def test_groups_list(self):
        actual = sorted(api_v2.groups_info_to_list(self.groups_data),
                        key=lambda x: x['id'])

        with open('tests/resources/v2/test_groups_list.json',
                  'r', encoding='utf-8') as file:
            expected = load(file)
            expected.sort(key=lambda x: x['id'])

        self.assertEqual(actual, expected, 'Invalid transformation')

    def test_groups_by_faculty(self):
        def sort_data(data: list):
            for item in data:
                item['groups'].sort(key=lambda x: x['id'])
            data.sort(key=lambda x: x['faculty'])

        actual = api_v2.groups_info_to_list(self.groups_data, True)
        sort_data(actual)

        with open('tests/resources/v2/test_groups_by_faculty.json',
                  'r', encoding='utf-8') as file:
            expected = load(file)
            sort_data(expected)

        self.assertEqual(actual, expected, 'Invalid transformation')

    def test_departments_list(self):
        actual = sorted(api_v2.departments_info_to_list(self.departments_data),
                        key=lambda x: x['id'])

        with open('tests/resources/v2/test_departments_list.json',
                  'r', encoding='utf-8') as file:
            expected = load(file)
            expected.sort(key=lambda x: x['id'])

        self.assertEqual(actual, expected, 'Invalid transformation')

    def test_departments_by_faculty(self):
        def sort_data(data: list):
            for item in data:
                item['departments'].sort(key=lambda x: x['id'])
            data.sort(key=lambda x: x['faculty'])

        actual = api_v2.departments_info_to_list(self.departments_data, True)
        sort_data(actual)

        with open('tests/resources/v2/test_departments_by_faculty.json',
                  'r', encoding='utf-8') as file:
            expected = load(file)
            sort_data(expected)

        self.assertEqual(actual, expected, 'Invalid transformation')
