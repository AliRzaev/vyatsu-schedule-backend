import argparse
from datetime import date
from json import dumps
from os import getenv
from typing import Sequence

from redis import Redis

from config.redis import KEY_GROUPS, KEY_RANGE_PREFIX, KEY_DEPARTMENTS, \
    KEY_DEPARTMENT_RANGE_PREFIX
from utils import groups_info, departments_info
from utils.date import as_date, get_moscow_today
from utils.extractors import *


def _get_nearest_range(today: date, ranges: Sequence[DateRange]):
    for range_ in reversed(ranges):
        if as_date(range_.first) <= today:
            return range_
    else:
        return ranges[0]


def prefetch(*,
             redis,
             groups_html: str = None,
             departments_html: str = None,
             force=False):
    return (prefetch_groups(redis=redis, html=groups_html, force=force),
            prefetch_departments(redis=redis, html=departments_html,
                                 force=force))


def prefetch_groups(*, redis, html: str = None, force=False):
    if redis.exists(KEY_GROUPS) and not force:
        return None

    if html is None:
        html = groups_info.get_page()

    groups = extract_groups(html, as_dict=True)
    ranges = extract_date_ranges(html)

    items = {KEY_GROUPS: dumps(tuple(groups.values()))}

    for group_id, ranges in ranges.items():
        name = groups[group_id].group
        autumn = [] if len(ranges['autumn']) == 0 else ranges['autumn'][-1]
        spring = [] if len(ranges['spring']) == 0 else ranges['spring'][-1]

        items[f'{KEY_RANGE_PREFIX}{group_id}'] = dumps((name, autumn, spring))

    redis.mset(items)

    return len(groups)


def prefetch_departments(*, redis, html: str = None, force=False):
    if redis.exists(KEY_DEPARTMENTS) and not force:
        return None

    if html is None:
        html = departments_info.get_page()

    departments = extract_departments(html, as_dict=True)
    ranges = extract_departments_date_ranges(html)

    items = {KEY_DEPARTMENTS: dumps(tuple(departments.values()))}

    for department_id, ranges in ranges.items():
        name = departments[department_id].department
        if len(ranges['autumn']) == 0:
            autumn = []
        else:
            autumn = _get_nearest_range(get_moscow_today(), ranges['autumn'])
        if len(ranges['spring']) == 0:
            spring = []
        else:
            spring = _get_nearest_range(get_moscow_today(), ranges['spring'])

        items[f'{KEY_DEPARTMENT_RANGE_PREFIX}{department_id}'] = \
            dumps((name, autumn, spring))

    redis.mset(items)

    return len(departments)


if __name__ == '__main__':
    REDIS_URL = getenv('REDIS_URL', '')
    if not REDIS_URL:
        raise ValueError('REDIS_URL is not defined')

    redis = Redis.from_url(REDIS_URL)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--force',
        help='Prefetch information even if it already exists',
        action='store_true'
    )

    args = parser.parse_args()
    status = prefetch(force=args.force, redis=redis)

    if status[0] is None and status[1] is None:
        print('Nothing to do')
    if status[0] is not None:
        print(f'{status[0]} groups were loaded')
    if status[1] is not None:
        print(f'{status[1]} departments were loaded')
