from unittest import TestCase

from server import app

from models import groups_info

from json import load, loads


class TestApiV1Groups(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        groups_info.delete_all()

        with open('tests/resources/test_groups_data.json', 'r', encoding='utf-8') as file:
            data = load(file)

        groups_info.upsert_documents([
            {
                'groupId': item['id'],
                'group': item['name'],
                'faculty': item['faculty']
            } for item in data
        ])

    def tearDown(self):
        groups_info.delete_all()

    def test_groups_list(self):
        response = self.app.get('/api/v1/groups/list')
        data = loads(response.data)

        with open('tests/resources/v1/test_groups_list.json', 'r', encoding='utf-8') as file:
            expected_data = load(file)

        self.assertEqual(data, expected_data, 'Invalid data')

    def test_groups_by_faculty(self):

        response = self.app.get('/api/v1/groups/by_faculty')
        data = loads(response.data)

        with open('tests/resources/v1/test_groups_by_faculty.json', 'r', encoding='utf-8') as file:
            expected_data = load(file)

        self.assertEqual(data, expected_data, 'Invalid data')


class TestApiV1Calls(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_calls(self):
        response = self.app.get('/api/v1/calls')

        with open('tests/resources/v1/test_calls.json', 'r', encoding='utf-8') as file:
            data = load(file)

        self.assertEqual(loads(response.data), data, 'Invalid data')
