import requests

from re import sub, compile
from typing import Dict, Union, Iterable, Optional, List
from datetime import timedelta
from collections import namedtuple

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from utils.cache import KeyValueStorage, RedisCollectionAdapter
from config.redis import get_instance

GROUPS_INFO_URL = 'https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html'

CACHE_PREFIX = __name__

_GROUPS_INFO_CACHE = KeyValueStorage(
    RedisCollectionAdapter(get_instance(), timedelta(days=1)))

_GROUP_NAMES_CACHE = KeyValueStorage(
    RedisCollectionAdapter(get_instance()))

SHORTHANDS = {
    'Институт биологии и биотехнологии (факультет)(ОРУ)': 'ИББТ',
    'Институт химии и экологии (факультет) (ОРУ)': 'ИнХимЭк',
    'Факультет автоматики и вычислительной техники (ОРУ)': 'ФАВТ',
    'Факультет истории, политических наук и культурологии (ОРУ)': 'ФИПНК',
    'Факультет компьютерных и физико-математических наук (ОРУ)': 'ФКиФМН',
    'Факультет менеджмента и сервиса (ОРУ)': 'ФМиС',
    'Факультет педагогики и психологии (ОРУ)': 'ФПП',
    'Факультет строительства и архитектуры (ОРУ)': 'ФСА',
    'Факультет технологий, инжиниринга и дизайна (ОРУ)': 'ФТИД',
    'Факультет физической культуры и спорта (ОРУ)': 'ФФКиС',
    'Факультет филологии и медиакоммуникаций (ОРУ)': 'ФФМ',
    'Факультет экономики и финансов (ОРУ)': 'ФЭиФ',
    'Электротехнический факультет (ОРУ)': 'ЭТФ',
    'Юридический институт (факультет) (ОРУ)': 'ЮИ'
}


GroupInfo = namedtuple('GroupInfo', ['group_id', 'group', 'faculty'])


def find_links_if(tag: Tag) -> bool:
    return tag.name == 'div' and 'grpPeriod' in tag['class']


def remove_parentheses(name: Union[NavigableString, str]) -> str:
    """
    Remove text in parentheses
    Example: 'Юридический институт (факультет) (ОРУ)' -> 'Юридический институт'
    """
    pattern = compile(r'\(.*?\)\s?')
    return sub(pattern, '', name).strip()


def get_groups_dict(tag: Tag) -> Dict[str, str]:
    """
    Find all occurrences of tags with links
    to groups schedules and return dictionary: {'group name': 'group id'}
    """
    return {remove_parentheses(link.string): link['data-grp_period_id'][:-1] for link in tag.find_all(find_links_if)}


def get_faculty_name_with_shorthand(faculty_name: str) -> str:
    stripped_name = remove_parentheses(faculty_name)
    if faculty_name in SHORTHANDS:
        return '{} ({})'.format(SHORTHANDS[faculty_name], stripped_name)
    else:
        return stripped_name


def parse_groups_info_page(html: str) -> Iterable[GroupInfo]:
    document = BeautifulSoup(html, 'html.parser')

    tables = document \
        .find(name='div', attrs={'class': 'column-center_rasp'}) \
        .find_all(name='table', attrs={'style': 'border: none !important;'})
    for table in tables:
        for faculty in (tag for tag in table.tbody.children if tag.name == 'tr'):
            faculty_name = faculty.find(name='div', attrs={'class': 'fak_name'}).string
            faculty_name = get_faculty_name_with_shorthand(faculty_name)

            for group_name, group_id in get_groups_dict(faculty).items():
                yield GroupInfo(group_id, group_name, faculty_name)


def get_groups_info() -> List[GroupInfo]:
    key = f'{CACHE_PREFIX}_groups_info_list'
    try:
        cached = _GROUPS_INFO_CACHE[key]
        return cached
    except KeyError:
        page = requests.get(GROUPS_INFO_URL).text
        data = list(parse_groups_info_page(page))
        _GROUPS_INFO_CACHE[key] = data
        return data


def get_groups_info_as_dict() -> Dict[str, GroupInfo]:
    key = f'{CACHE_PREFIX}_groups_info_dict'
    try:
        cached = _GROUPS_INFO_CACHE[key]
        return cached
    except KeyError:
        page = requests.get(GROUPS_INFO_URL).text
        data = {item.group_id: item for item in parse_groups_info_page(page)}
        _GROUPS_INFO_CACHE[key] = data
        return data


def get_group_name(group_id: str) -> Optional[str]:
    key = f'{CACHE_PREFIX}_group_name_{group_id}'
    try:
        cached = _GROUP_NAMES_CACHE[key]
        return cached
    except KeyError:
        groups_info = get_groups_info_as_dict()
        if group_id in groups_info:
            group_name = groups_info[group_id].group
            _GROUP_NAMES_CACHE[key] = group_name
            return group_name
        else:
            return None
