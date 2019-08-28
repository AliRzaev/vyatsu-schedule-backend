from json import load

from loguru import logger
from pytest import fixture

import config
from server import create_app
from utils.extractors import GroupInfo, DateRange, DepartmentInfo, \
    extract_groups, extract_date_ranges, extract_departments
from utils.repository import get_repository


@fixture(scope='session')
def groups_page():
    with open('tests/resources/html/groups_info_page.html',
              'r', encoding='utf-8') as file:
        return file.read()


@fixture(scope='session')
def groups_info():
    with open('tests/resources/groups_info.json',
              'r', encoding='utf-8') as file:
        return sorted(GroupInfo(item['groupId'], item['group'], item['faculty'])
                      for item in load(file))


@fixture(scope='session')
def groups_ranges():
    with open('tests/resources/date_ranges.json',
              'r', encoding='utf-8') as file:
        groups_ranges = load(file)
        for seasons in groups_ranges.values():
            seasons['autumn'] = [
                DateRange(*range_) for range_ in seasons['autumn']
            ]
            seasons['spring'] = [
                DateRange(*range_) for range_ in seasons['spring']
            ]

        return groups_ranges


@fixture(scope='session')
def departments_page():
    with open('tests/resources/html/departments_info_page.html',
              'r', encoding='utf-8') as file:
        return file.read()


@fixture(scope='session')
def departments_info():
    with open('tests/resources/departments_info.json',
              'r', encoding='utf-8') as file:
        return sorted(DepartmentInfo(item['departmentId'], item['department'],
                                     item['faculty'])
                      for item in load(file))


@fixture(scope='session')
def departments_ranges():
    with open('tests/resources/departments_date_ranges.json',
              'r', encoding='utf-8') as file:
        departments_ranges = load(file)
        for seasons in departments_ranges.values():
            seasons['autumn'] = [
                DateRange(*range_) for range_ in seasons['autumn']
            ]
            seasons['spring'] = [
                DateRange(*range_) for range_ in seasons['spring']
            ]

        return departments_ranges


@fixture(scope='session')
def groups_list_v1():
    with open('tests/resources/v1/test_groups_list.json',
              'r', encoding='utf-8') as file:
        return load(file)


@fixture(scope='session')
def groups_by_faculty_v1():
    with open('tests/resources/v1/test_groups_by_faculty.json',
              'r', encoding='utf-8') as file:
        return load(file)


@fixture(scope='session')
def groups_list_v2():
    with open('tests/resources/v2/test_groups_list.json',
              'r', encoding='utf-8') as file:
        groups = load(file)
        groups.sort(key=lambda x: x['name'])

        return groups


@fixture(scope='session')
def groups_by_faculty_v2():
    def sort_data(data: list):
        for item in data:
            item['groups'].sort(key=lambda x: x['name'])
        data.sort(key=lambda x: x['faculty'])

    with open('tests/resources/v2/test_groups_by_faculty.json',
              'r', encoding='utf-8') as file:
        groups = load(file)
        sort_data(groups)

        return groups


@fixture(scope='session')
def departments_list_v2():
    with open('tests/resources/v2/test_departments_list.json',
              'r', encoding='utf-8') as file:
        departments = load(file)
        departments.sort(key=lambda x: x['name'])

        return departments


@fixture(scope='session')
def departments_by_faculty_v2():
    def sort_data(data: list):
        for item in data:
            item['departments'].sort(key=lambda x: x['name'])
        data.sort(key=lambda x: x['faculty'])

    with open('tests/resources/v2/test_departments_by_faculty.json',
              'r', encoding='utf-8') as file:
        departments = load(file)
        sort_data(departments)

        return departments


@fixture(scope='session')
def calls_v1():
    with open('tests/resources/v1/test_calls.json',
              'r', encoding='utf-8') as file:
        return load(file)


@fixture(scope='session')
def calls_v2():
    with open('tests/resources/v2/test_calls.json',
              'r', encoding='utf-8') as file:
        return load(file)


@fixture(scope='function')
def flask_app():
    return create_app(config.TestingConfig())


@fixture(scope='session')
def prefetch_groups(groups_page):
    def _prefetch_groups():
        groups = extract_groups(groups_page)
        groups_date_ranges = extract_date_ranges(groups_page)

        get_repository().update_groups_info(groups, groups_date_ranges, True)

    return _prefetch_groups


@fixture(scope='session')
def prefetch_departments(departments_page):
    def _prefetch_departments():
        departments = extract_departments(departments_page)
        departments_date_ranges = extract_date_ranges(departments_page)

        get_repository().update_departments_info(departments,
                                                 departments_date_ranges, True)

    return _prefetch_departments


@fixture(autouse=True)
def disable_logger():
    logger.disable('server')
    yield
    logger.enable('server')
