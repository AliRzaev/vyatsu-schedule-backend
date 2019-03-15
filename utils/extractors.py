import re
from collections import defaultdict, namedtuple
from functools import lru_cache
from re import sub, compile
from typing import Iterable, Union, Dict

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from utils.date import as_date

GroupInfo = namedtuple('GroupInfo', ['group_id', 'group', 'faculty'])

DepartmentInfo = namedtuple('DepartmentInfo',
                            ['department_id', 'department', 'faculty'])

DateRange = namedtuple('DateRange', ['first', 'second'])

SHORTHANDS = {
    'Институт биологии и биотехнологии (факультет)(ОРУ)': 'ИББТ',
    'Институт химии и экологии (факультет) (ОРУ)': 'ИнХимЭк',
    'Факультет автоматики и вычислительной техники (ОРУ)': 'ФАВТ',
    'Факультет истории, политических наук и культурологии (ОРУ)': 'ФИПНК',
    'Факультет компьютерных и физико-математических наук (ОРУ)': 'ФКФМН',
    'Факультет лингвистики (ОРУ)': 'ФЛ',
    'Факультет менеджмента и сервиса (ОРУ)': 'ФМиС',
    'Факультет педагогики и психологии (ОРУ)': 'ФПП',
    'Факультет строительства и архитектуры (ОРУ)': 'ФСА',
    'Факультет технологий, инжиниринга и дизайна (ОРУ)': 'ФТИД',
    'Факультет физической культуры и спорта (ОРУ)': 'ФФКС',
    'Факультет филологии и медиакоммуникаций (ОРУ)': 'ФФМ',
    'Факультет экономики и финансов (ОРУ)': 'ФЭиФ',
    'Электротехнический факультет (ОРУ)': 'ЭТФ',
    'Юридический институт (факультет) (ОРУ)': 'ЮИ'
}

GROUP_PATTERN = re.compile(
    r'/reports/schedule/Group/(\d{4,})_([12])_(\d{8})_(\d{8})\.pdf'
)
DEPARTMENT_PATTERN = re.compile(
    r'/reports/schedule/prepod/(\d{2,})_([12])_(\d{8})_(\d{8})\.html'
)


def _remove_parenthesized(name: Union[NavigableString, str]) -> str:
    """
    Remove text in parentheses. Parentheses will be also removed.

    Example: 'Юридический институт (факультет) (ОРУ)' -> 'Юридический институт'
    """
    pattern = compile(r'\(.*?\)\s?')
    return sub(pattern, '', name).strip()


def _faculty_with_shorthand(faculty_name: str) -> str:
    """
    Construct string of the faculty name shorthand followed by
    faculty name in parentheses.
    """
    stripped_name = _remove_parenthesized(faculty_name)
    if faculty_name in SHORTHANDS:
        return '{} ({})'.format(SHORTHANDS[faculty_name], stripped_name)
    else:
        return stripped_name


def _groups_as_dict(tag: Tag) -> Dict[str, str]:
    """
    Find all occurrences of tags with links
    to groups schedules and return dictionary: {'group name': 'group id'}
    """

    def _find_links_if(link: Tag) -> bool:
        return link.name == 'div' and 'grpPeriod' in link['class']

    return {_remove_parenthesized(link.string): link['data-grp_period_id'][:-1]
            for link in tag.find_all(_find_links_if)}


def _extract_groups(html: str) -> Iterable[GroupInfo]:
    """
    Yield GroupInfo items extracted from html page.
    """
    document = BeautifulSoup(html, 'html.parser')

    tables = document \
        .find(name='div', attrs={'class': 'column-center_rasp'}) \
        .find_all(name='table', attrs={'style': 'border: none !important;'})
    for table in tables:
        faculties = (tag for tag in table.tbody.children if tag.name == 'tr')
        for faculty in faculties:
            faculty_tag = faculty.find(name='div',
                                       attrs={'class': 'fak_name'})
            faculty_name = _faculty_with_shorthand(faculty_tag.string)

            for name, id_ in _groups_as_dict(faculty).items():
                yield GroupInfo(id_, name, faculty_name)


def _extract_departments(html: str) -> Iterable[DepartmentInfo]:
    """
    Yield DepartmentInfo items extracted from html page.
    """
    document = BeautifulSoup(html, 'html.parser')

    tables = document \
        .find(name='div', attrs={'class': 'column-center_rasp'}) \
        .find_all(name='table', attrs={'style': 'border: none !important;'})

    for table in tables:
        faculties = (tag for tag in table.tbody.children if tag.name == 'tr')
        for faculty in faculties:
            name_tag = faculty.find(name='div',
                                    attrs={'class': 'fak_name'})
            faculty_id = name_tag['data-fak_id']
            faculty_tag = faculty.find(name='div',
                                       attrs={'id': f'fak_id_{faculty_id}'})
            faculty_name = _faculty_with_shorthand(name_tag.string)
            departments = (tag for tag in faculty_tag.table.tbody.children
                           if tag.name == 'tr' and tag.find(name='div'))
            for department in departments:
                department_tag = department.find(name='div',
                                                 attrs={'class': 'kafPeriod'})
                department_name = _remove_parenthesized(department_tag.string)
                department_id = department_tag['data-kaf_period_id'][:-1]

                yield DepartmentInfo(department_id, department_name,
                                     faculty_name)


@lru_cache()
def extract_departments(html: str, as_dict=False):
    """
    Extract information about departments from html page.

    :rtype: Union[Tuple[DepartmentInfo], Dict[str, DepartmentInfo]]
    """
    if as_dict:
        return {
            item.department_id: item for item in _extract_departments(html)
        }
    else:
        return tuple(_extract_departments(html))


@lru_cache()
def extract_groups(html: str, as_dict=False):
    """
    Extract information about groups from html page.

    :rtype: Union[Tuple[GroupInfo], Dict[str, GroupInfo]]
    """
    if as_dict:
        return {
            group.group_id: group for group in _extract_groups(html)
        }
    else:
        return tuple(_extract_groups(html))


@lru_cache()
def extract_departments_date_ranges(html: str):
    """
    Extract information about departments date ranges from html page.

    Returns a dict object of the following structure: ::

      {
        '<department_id>': {
          'autumn': [DateRange(<first>, <second>), ...],
          'spring': [DateRange(<first>, <second>), ...]
        },
        ...
      }
    """
    date_ranges = defaultdict(lambda: dict(autumn=list(), spring=list()))

    for match in re.finditer(DEPARTMENT_PATTERN, html):
        department_id, season, first, second = match.groups()
        season = 'autumn' if season == '1' else 'spring'

        date_ranges[department_id][season].append(DateRange(first, second))

    for seasons in date_ranges.values():
        for ranges in seasons.values():
            ranges.sort(key=lambda x: as_date(x.first))

    return date_ranges


@lru_cache()
def extract_date_ranges(html: str):
    """
    Extract information about schedules date ranges from html page.

    Returns a dict object of the following structure: ::

      {
        '<group_id>': {
          'autumn': [DateRange(<first>, <second>), ...],
          'spring': [DateRange(<first>, <second>), ...]
        },
        ...
      }
    """
    date_ranges = defaultdict(lambda: dict(autumn=list(), spring=list()))

    for match in re.finditer(GROUP_PATTERN, html):
        group_id, season, first, second = match.groups()
        season = 'autumn' if season == '1' else 'spring'
        date_ranges[group_id][season].append(DateRange(first, second))

    for seasons in date_ranges.values():
        for ranges in seasons.values():
            ranges.sort(key=lambda x: as_date(x.first))

    return date_ranges


__all__ = [
    'DepartmentInfo', 'GroupInfo', 'DateRange',
    'extract_date_ranges', 'extract_groups',
    'extract_departments_date_ranges', 'extract_departments',
    'SHORTHANDS', 'GROUP_PATTERN', 'DEPARTMENT_PATTERN'
]
