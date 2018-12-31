from json import load
from unittest import TestCase

from utils.extractors import extract_date_ranges, extract_groups, GroupInfo, \
    DateRange


class TestExtractors(TestCase):

    def setUp(self):
        with open('tests/resources/html/groups_info_page.html',
                  'r', encoding='utf-8') as file:
            self.page = file.read()

        with open('tests/resources/groups_info.json',
                  'r', encoding='utf-8') as file:
            self.info = sorted(
                (GroupInfo(item['groupId'], item['group'], item['faculty'])
                 for item in load(file)))

        with open('tests/resources/date_ranges.json',
                  'r', encoding='utf-8') as file:
            self.ranges = load(file)
            for seasons in self.ranges.values():
                seasons['autumn'] = [
                    DateRange(*range_) for range_ in seasons['autumn']
                ]
                seasons['spring'] = [
                    DateRange(*range_) for range_ in seasons['spring']
                ]

    def test_extract_groups(self):
        actual = sorted(extract_groups(self.page))
        expected = self.info

        self.assertEqual(actual, expected, 'Data mismatch')

    def test_extract_date_ranges(self):
        actual = extract_date_ranges(self.page)
        expected = self.ranges

        self.assertEqual(actual, expected)
