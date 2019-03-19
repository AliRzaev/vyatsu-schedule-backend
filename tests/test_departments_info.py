from datetime import date
from json import load
from unittest import TestCase

import responses

from utils.date import get_date_of_weekday
from utils.departments_info import DEPARTMENTS_INFO_URL, _get_page
from utils.extractors import *


class TestDepartmentsInfo(TestCase):

    def setUp(self):
        with open('tests/resources/html/departments_info_page.html',
                  'r', encoding='utf-8') as file:
            self.page = file.read()

        with open('tests/resources/departments_info.json',
                  'r', encoding='utf-8') as file:
            self.info = sorted(
                (DepartmentInfo(item['departmentId'],
                                item['department'],
                                item['faculty'])
                 for item in load(file)))

        self.clear_cache()

    def tearDown(self):
        self.clear_cache()

    def clear_cache(self):
        _get_page.cache_clear()

    @responses.activate
    def test_get_departments_threshold(self):
        self.clear_cache()
        responses.add(responses.GET, DEPARTMENTS_INFO_URL, self.page,
                      content_type='text/html; charset=utf8')

        d = date(2018, 12, 5)
        _get_page(d)

        self.assertEqual(len(responses.calls), 1)

        _get_page(d)

        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_departments_threshold_invalidate(self):
        self.clear_cache()
        responses.add(responses.GET, DEPARTMENTS_INFO_URL, self.page,
                      content_type='text/html; charset=utf8')

        d = date(2018, 12, 5)  # Wednesday
        _get_page(d)

        self.assertEqual(len(responses.calls), 1)

        _get_page(get_date_of_weekday(2, date(2018, 12, 6)))  # next Wednesday

        self.assertEqual(len(responses.calls), 2)
