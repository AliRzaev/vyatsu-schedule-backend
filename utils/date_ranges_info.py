import re
import requests
from datetime import date, timedelta
from typing import Tuple, Optional

from utils.wrappers import comparable_mixin
from utils.redis_config import get_instance
from utils.cache import KeyValueStorage, RedisCollectionAdapter
from utils.groups_info import GROUPS_INFO_URL

P_AUTUMN = r'/reports/schedule/Group/group_id_1_(\d{8})_(\d{8})\.pdf'
P_SPRING = r'/reports/schedule/Group/group_id_2_(\d{8})_(\d{8})\.pdf'
PATTERN = re.compile(r'/reports/schedule/Group/(\d{4,})_([12])_(\d{8})_(\d{8})\.pdf')

CACHE_PREFIX = __name__

_DATE_RANGES_CACHE = KeyValueStorage(
    RedisCollectionAdapter(get_instance(), timedelta(days=1)))


@comparable_mixin
class DateRange:

    def __init__(self, first: str, second: str):
        self.first = first
        self.second = second

        d = int(first[:2])
        m = int(first[2:4])
        y = int(first[4:])
        self.first_date = date(y, m, d)

    def __lt__(self, other):
        return self.first_date < other.first_date


def get_all_date_ranges(html: str):
    def init_dict_item(dict_, group_id):
        dict_[group_id] = {
            'autumn': [],
            'spring': []
        }

    date_ranges = dict()

    for match in re.finditer(PATTERN, html):
        group_id, season, first, second = match.groups()
        season = 'autumn' if season == '1' else 'spring'
        if group_id not in date_ranges:
            init_dict_item(date_ranges, group_id)
        date_ranges[group_id][season].append(DateRange(first, second))

    return date_ranges


def get_date_range(group_id: str, season: str,
                   today: date = None) -> Optional[Tuple[str, str]]:
    if today is None:
        today = date.today()
    key = f'{CACHE_PREFIX}_ranges'
    try:
        date_ranges = _DATE_RANGES_CACHE[key]
    except KeyError:
        page = requests.get(GROUPS_INFO_URL).text
        date_ranges = get_all_date_ranges(page)
        _DATE_RANGES_CACHE[key] = date_ranges

    if group_id not in date_ranges or season not in date_ranges[group_id]:
        return None

    filtered_ranges = [
        range_ for range_ in sorted(date_ranges[group_id][season])
        if range_.first_date < today
    ]

    if len(filtered_ranges) == 0:
        return None
    else:
        nearest_range = filtered_ranges[-1]
        return nearest_range.first, nearest_range.second
