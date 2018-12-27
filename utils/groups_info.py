from bisect import bisect_right
from datetime import date
from functools import lru_cache
from typing import Dict, Optional, Tuple

import requests

from utils.date import get_date_of_weekday, as_date
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
    return extract_groups(get_page())


def get_groups_as_dict() -> Dict[str, GroupInfo]:
    return extract_groups(get_page(), as_dict=True)


def get_group_name(group_id: str) -> Optional[str]:
    groups_info = get_groups_as_dict()
    return groups_info.get(group_id, None)


def get_date_range(group_id: str,
                   season: str,
                   today: date = None) -> Optional[DateRange]:
    if today is None:
        today = date.today()

    date_ranges = extract_date_ranges(get_page())

    if group_id not in date_ranges or season not in date_ranges[group_id]:
        return None

    ranges = date_ranges[group_id][season]
    ranges_keys = [as_date(range_.first) for range_ in ranges]

    index = bisect_right(ranges_keys, today)
    if index:
        return ranges[index-1]
    else:
        return None
