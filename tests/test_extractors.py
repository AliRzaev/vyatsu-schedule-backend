from json import load
from unittest import TestCase

from utils.extractors import extract_date_ranges, extract_groups, GroupInfo, \
    DateRange, DepartmentInfo, extract_departments, \
    extract_departments_date_ranges


class TestExtractors(TestCase):

    def setUp(self):
        with open('tests/resources/html/groups_info_page.html',
                  'r', encoding='utf-8') as file:
            self.groups_page = file.read()

        with open('tests/resources/groups_info.json',
                  'r', encoding='utf-8') as file:
            self.groups_info = sorted(
                (GroupInfo(item['groupId'], item['group'], item['faculty'])
                 for item in load(file)))

        with open('tests/resources/html/departments_info_page.html',
                  'r', encoding='utf-8') as file:
            self.departments_page = file.read()

        with open('tests/resources/departments_info.json',
                  'r', encoding='utf-8') as file:
            self.departments_info = sorted(
                (DepartmentInfo(item['departmentId'], item['department'],
                                item['faculty'])
                 for item in load(file)))

        with open('tests/resources/date_ranges.json',
                  'r', encoding='utf-8') as file:
            self.groups_ranges = load(file)
            for seasons in self.groups_ranges.values():
                seasons['autumn'] = [
                    DateRange(*range_) for range_ in seasons['autumn']
                ]
                seasons['spring'] = [
                    DateRange(*range_) for range_ in seasons['spring']
                ]

        with open('tests/resources/departments_date_ranges.json',
                  'r', encoding='utf-8') as file:
            self.departments_ranges = load(file)
            for seasons in self.departments_ranges.values():
                seasons['autumn'] = [
                    DateRange(*range_) for range_ in seasons['autumn']
                ]
                seasons['spring'] = [
                    DateRange(*range_) for range_ in seasons['spring']
                ]

    def test_extract_groups(self):
        actual = sorted(extract_groups(self.groups_page))
        expected = self.groups_info

        self.assertEqual(actual, expected, 'Data mismatch')

    def test_extract_date_ranges(self):
        actual = extract_date_ranges(self.groups_page)
        expected = self.groups_ranges

        self.assertEqual(actual, expected)

    def test_extract_departments(self):
        actual = sorted(extract_departments(self.departments_page))
        expected = self.departments_info

        self.assertEqual(actual, expected, 'Data mismatch')

    def test_extract_departments_date_ranges(self):
        actual = extract_departments_date_ranges(self.departments_page)
        expected = self.departments_ranges

        self.assertEqual(actual, expected)
