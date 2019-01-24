import argparse
from json import dumps

from config.redis import get_instance, KEY_GROUPS, KEY_RANGE_PREFIX
from utils.extractors import *
from utils.groups_info import get_page


def prefetch(*, html: str = None, force=False):
    redis = get_instance()

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--force',
        help='Prefetch information even if it already exists',
        action='store_true'
    )

    args = parser.parse_args()
    status = prefetch(force=args.force)

    if status is None:
        print('Nothing to do')
    else:
        print(f'{status} groups were loaded')
