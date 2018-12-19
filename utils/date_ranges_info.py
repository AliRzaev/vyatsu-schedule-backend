import re
from datetime import date
from typing import Tuple, Optional

from utils.wrappers import comparable_mixin

P_AUTUMN = r'/reports/schedule/Group/group_id_1_(\d{8})_(\d{8})\.pdf'
P_SPRING = r'/reports/schedule/Group/group_id_2_(\d{8})_(\d{8})\.pdf'


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


def get_date_range(
        html: str, group_id: str,
        season: str, today: date = None) -> Optional[Tuple[str, str]]:
    if season == 'autumn':
        pattern = P_AUTUMN.replace('group_id', group_id)
    elif season == 'spring':
        pattern = P_SPRING.replace('group_id', group_id)
    else:
        raise ValueError(f'Unknown season: {season}')

    if today is None:
        today = date.today()

    all_date_ranges = sorted(
        DateRange(*match.groups()) for match in re.finditer(pattern, html)
    )
    filtered_ranges = [
        range_ for range_ in all_date_ranges if range_.first_date < today
    ]

    if len(filtered_ranges) == 0:
        return None
    else:
        nearest_range = filtered_ranges[-1]
        return nearest_range.first, nearest_range.second
