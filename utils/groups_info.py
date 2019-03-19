from datetime import date
from functools import lru_cache
from json import loads
from typing import Dict, Optional, Tuple

import requests

from config.redis import redis_store, KEY_GROUPS, KEY_RANGE_PREFIX
from utils.date import get_date_of_weekday
from utils.extractors import *

GROUPS_INFO_URL = 'https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya' \
                  '/raspisanie-zanyatiy-dlya-studentov.html'


# threshold parameter is used to distinguish function
# invocations over time
@lru_cache()
def _get_page(threshold: date) -> str:
    response = requests.get(GROUPS_INFO_URL)
    return response.text


def get_page() -> str:
    threshold = get_date_of_weekday(3)
    return _get_page(threshold)


def get_groups() -> Tuple[GroupInfo, ...]:
    data = loads(redis_store.get(KEY_GROUPS))
    return tuple(GroupInfo(*args) for args in data)


def get_groups_as_dict() -> Dict[str, GroupInfo]:
    data = loads(redis_store.get(KEY_GROUPS))
    return {
        id_: GroupInfo(id_, name, faculty) for id_, name, faculty in data
    }


def get_group_name(group_id: str) -> Optional[str]:
    key = f'{KEY_RANGE_PREFIX}{group_id}'
    value = redis_store.get(key)

    if value is None:
        return None

    group_info = loads(value)
    return group_info[0]


def get_date_range(group_id: str, season: str) -> Optional[DateRange]:
    key = f'{KEY_RANGE_PREFIX}{group_id}'
    _, autumn, spring = loads(redis_store.get(key))

    if season == 'autumn':
        range_ = autumn
    else:
        range_ = spring

    if len(range_) != 0:
        return DateRange(*range_)
    else:
        return None
