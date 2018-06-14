from json import load
from unittest import TestCase

from utils.transforming import api_v1, api_v2


class TestTransformingV1(TestCase):

    def setUp(self):
        with open('tests/resources/test_groups_data.json', 'r', encoding='utf-8') as file:
            data = load(file)

        self.data = [
            {
                'groupId': item['id'],
                'group': item['name'],
                'faculty': item['faculty']
            } for item in data
        ]

    def test_groups_list(self):
        data = api_v1.groups_info_to_dict(self.data)

        with open('tests/resources/v1/test_groups_list.json', 'r', encoding='utf-8') as file:
            expected_data = load(file)

        self.assertEqual(data, expected_data, 'Invalid transformation')

    def test_groups_by_faculty(self):
        data = api_v1.groups_info_to_dict(self.data, True)

        with open('tests/resources/v1/test_groups_by_faculty.json', 'r', encoding='utf-8') as file:
            expected_data = load(file)

        self.assertEqual(data, expected_data, 'Invalid transformation')


class TestTransformingV2(TestCase):

    def setUp(self):
        with open('tests/resources/test_groups_data.json', 'r', encoding='utf-8') as file:
            data = load(file)

        self.data = [
            {
                'groupId': item['id'],
                'group': item['name'],
                'faculty': item['faculty']
            } for item in data
        ]

    def test_groups_list(self):
        data = sorted(api_v2.groups_info_to_list(self.data), key=lambda x: x['id'])

        with open('tests/resources/v2/test_groups_list.json', 'r', encoding='utf-8') as file:
            expected_data = load(file)
            expected_data.sort(key=lambda x: x['id'])

        self.assertEqual(data, expected_data, 'Invalid transformation')

    def test_groups_by_faculty(self):
        def sort_data(data: list):
            for item in data:
                item['groups'].sort(key=lambda x: x['id'])
            data.sort(key=lambda x: x['faculty'])

        data = api_v2.groups_info_to_list(self.data, True)
        sort_data(data)

        with open('tests/resources/v2/test_groups_by_faculty.json', 'r', encoding='utf-8') as file:
            expected_data = load(file)
            sort_data(expected_data)

        self.assertEqual(data, expected_data, 'Invalid data')
