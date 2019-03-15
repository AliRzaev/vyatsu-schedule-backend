from datetime import date
from functools import lru_cache
from json import loads
from typing import Dict, Optional, Tuple

import requests

from config.redis import redis_store, KEY_DEPARTMENTS, \
    KEY_DEPARTMENT_RANGE_PREFIX
from utils.date import get_date_of_weekday
from utils.extractors import *

DEPARTMENTS_INFO_URL = 'https://www.vyatsu.ru/studentu-1/' \
                       'spravochnaya-informatsiya/teacher.html'


# threshold parameter is used to distinguish function
# invocations over time
@lru_cache()
def _get_page(threshold: date) -> str:
    response = requests.get(DEPARTMENTS_INFO_URL)
    return response.text


def get_page() -> str:
    threshold = get_date_of_weekday(3)
    return _get_page(threshold)


def get_departments() -> Tuple[DepartmentInfo, ...]:
    data = loads(redis_store.get(KEY_DEPARTMENTS))
    return tuple(DepartmentInfo(*args) for args in data)


def get_departments_as_dict() -> Dict[str, DepartmentInfo]:
    data = loads(redis_store.get(KEY_DEPARTMENTS))
    return {
        id_: DepartmentInfo(id_, name, faculty) for id_, name, faculty in data
    }


def get_department_name(department_id: str) -> Optional[str]:
    key = f'{KEY_DEPARTMENT_RANGE_PREFIX}{department_id}'
    value = redis_store.get(key)

    if value is None:
        return None

    department_info = loads(value)
    return department_info[0]


def get_date_range(department_id: str, season: str) -> Optional[DateRange]:
    key = f'{KEY_DEPARTMENT_RANGE_PREFIX}{department_id}'
    _, autumn, spring = loads(redis_store.get(key))

    if season == 'autumn':
        range_ = autumn
    else:
        range_ = spring

    if len(range_) != 0:
        return DateRange(*range_)
    else:
        return None
