from re import sub, compile
from typing import Dict, Union, Tuple, Iterable

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

URL = 'https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html'

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
        return '({}) {}'.format(SHORTHANDS[faculty_name], stripped_name)
    else:
        return stripped_name


def get_groups_with_faculty(url: str) -> Iterable[Tuple[str, str, str]]:
    document = BeautifulSoup(requests.get(url).content.decode('utf-8'), 'html.parser')

    tables = document \
        .find(name='div', attrs={'class': 'column-center_rasp'}) \
        .find_all(name='table', attrs={'style': 'border: none !important;'})
    for table in tables:
        for faculty in (tag for tag in table.tbody.children if tag.name == 'tr'):
            faculty_name = faculty.find(name='div', attrs={'class': 'fak_name'}).string
            faculty_name = get_faculty_name_with_shorthand(faculty_name)

            for group_name, group_id in get_groups_dict(faculty).items():
                yield (faculty_name, group_name, group_id)


def update_groups(url: str):
    from models import groups_info

    documents = [
        {
            "groupId": group_id,
            "group": group_name,
            "faculty": faculty
        } for faculty, group_name, group_id in get_groups_with_faculty(url)
    ]
    groups_info.upsert_documents(documents)


if __name__ == '__main__':
    update_groups(URL)
