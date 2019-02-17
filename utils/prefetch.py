import argparse
from json import dumps
from os import getenv

from redis import Redis

from config.redis import KEY_GROUPS, KEY_RANGE_PREFIX
from utils.extractors import *
from utils.groups_info import get_page


def prefetch(*, redis, html: str = None, force=False):
    if redis.exists(KEY_GROUPS) and not force:
        return None

    if html is None:
        html = get_page()

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

    if status is None:
        print('Nothing to do')
    else:
        print(f'{status} groups were loaded')
