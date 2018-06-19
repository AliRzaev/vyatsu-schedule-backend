import re
import requests
import argparse
from utils.date import get_current_season
from utils.wrappers import comparable_mixin
from datetime import date
from typing import Pattern, Dict, Tuple

P_AUTUMN = re.compile(r'/reports/schedule/Group/(\d{4})_1_(\d{8})_(\d{8})\.pdf')
P_SPRING = re.compile(r'/reports/schedule/Group/(\d{4})_2_(\d{8})_(\d{8})\.pdf')

URL = 'https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html'


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


def get_date_ranges(pattern: Pattern) -> Dict[str, Tuple[str, str]]:
    html = requests.get(URL).text

    date_ranges = dict()

    for match in re.finditer(pattern, html):
        group_id, first, second = match.groups()
        new_range = DateRange(first, second)

        if group_id not in date_ranges:
            date_ranges[group_id] = new_range
        elif new_range > date_ranges[group_id]:
            date_ranges[group_id] = new_range

    return {group_id: (date_range.first, date_range.second) for group_id, date_range in date_ranges.items()}


def update_date_ranges(season: str):
    from models import schedule_ranges

    if season == 'autumn':
        data = get_date_ranges(P_AUTUMN)
    elif season == 'spring':
        data = get_date_ranges(P_SPRING)
    else:
        raise ValueError(f'Unknown season: {season}')

    documents = [
        {
            'groupId': group_id,
            'season': season,
            'range': _range
        } for group_id, _range in data.items()
    ]
    schedule_ranges.upsert_documents(documents)


def build_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--force',
        help='Update schedule ranges for ALL groups, for ALL seasons',
        action='store_true'
    )
    parser.add_argument(
        '-d',
        '--drop-old',
        help='Delete ALL schedule ranges from DB before updating',
        action='store_true'
    )

    return parser


if __name__ == '__main__':
    from models import schedule_ranges

    parser = build_arg_parser()
    args = parser.parse_args()

    force = args.force
    drop_old = args.drop_old
    season = get_current_season()

    if drop_old:
        schedule_ranges.delete_all()

    if force:
        update_date_ranges('autumn')
        update_date_ranges('spring')
    else:
        update_date_ranges(season)
