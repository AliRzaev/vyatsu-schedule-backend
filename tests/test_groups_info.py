from unittest import TestCase
from utils.groups_info import *
from json import load


class TestGroupsInfo(TestCase):

    def setUp(self):
        with open(
                'tests/resources/html/groups_info_page.html', 'r',
                encoding='utf-8') as file:
            self.page = file.read()

        with open(
                'tests/resources/groups_info.json', 'r',
                encoding='utf-8') as file:
            self.info = load(file)

    def test_remove_parentheses(self):
        data = (
            ('Юридический институт (факультет) (ОРУ)', 'Юридический институт'),
            ('Юридический институт (факультет)', 'Юридический институт'),
            ('Юридический институт', 'Юридический институт')
        )

        for item in data:
            with self.subTest(item=item):
                s = remove_parentheses(item[0])
                self.assertTrue(s, item[1])

    def test_groups_info(self):
        actual = sorted(get_groups_info(self.page), key=lambda x: x['groupId'])
        expected = sorted(self.info, key=lambda x: x['groupId'])

        self.assertEqual(actual, expected)
