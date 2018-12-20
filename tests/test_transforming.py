from json import load
from unittest import TestCase

from utils.transforming import api_v1, api_v2
from utils.groups_info import GroupInfo


class TestTransformingV1(TestCase):

    def setUp(self):
        with open('tests/resources/groups_info.json',
                  'r', encoding='utf-8') as file:
            self.data = [GroupInfo(item['groupId'],
                                   item['group'],
                                   item['faculty']) for item in load(file)]

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
            self.data = [GroupInfo(item['groupId'],
                                   item['group'],
                                   item['faculty']) for item in load(file)]

    def test_groups_list(self):
        actual = sorted(api_v2.groups_info_to_list(self.data),
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

        actual = api_v2.groups_info_to_list(self.data, True)
        sort_data(actual)

        with open('tests/resources/v2/test_groups_by_faculty.json',
                  'r', encoding='utf-8') as file:
            expected = load(file)
            sort_data(expected)

        self.assertEqual(actual, expected, 'Invalid data')
