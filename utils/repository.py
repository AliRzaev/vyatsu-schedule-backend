from json import loads, dumps
from typing import Tuple, Dict, Optional, Sequence

from flask import g

import databases
from utils import date
from utils.date import get_moscow_today, as_date
from utils.extractors import GroupInfo, DateRange, DepartmentInfo


class Repository:
    KEY_GROUPS = 'groups'

    KEY_DEPARTMENTS = 'departments'

    KEY_RANGE_PREFIX = 'group_'
    """
    Key prefix for group's date range. The whole key is something like 'group_1234'
    """

    KEY_DEPARTMENT_RANGE_PREFIX = 'department_'
    """
    Key prefix for department's date range.
    The whole key is something like 'department_1234'
    """

    def __init__(self, redis_store):
        self._redis_store = redis_store

    def get_groups(self) -> Tuple[GroupInfo, ...]:
        data = loads(self._redis_store.get(Repository.KEY_GROUPS)) or []
        return tuple(GroupInfo(*args) for args in data)

    def get_groups_as_dict(self) -> Dict[str, GroupInfo]:
        data = loads(self._redis_store.get(Repository.KEY_GROUPS)) or []
        return {
            id_: GroupInfo(id_, name, faculty) for id_, name, faculty in data
        }

    def get_group_name(self, group_id: str) -> Optional[str]:
        key = f'{Repository.KEY_RANGE_PREFIX}{group_id}'
        value = self._redis_store.get(key)

        if value is None:
            return None

        group_info = loads(value)
        return group_info[0]

    def get_group_date_range(self, group_id: str, season: str) -> Optional[DateRange]:
        key = f'{Repository.KEY_RANGE_PREFIX}{group_id}'
        return self._get_date_range(key, season)

    def get_departments(self) -> Tuple[DepartmentInfo, ...]:
        data = loads(self._redis_store.get(Repository.KEY_DEPARTMENTS)) or []
        return tuple(DepartmentInfo(*args) for args in data)

    def get_departments_as_dict(self) -> Dict[str, DepartmentInfo]:
        data = loads(self._redis_store.get(Repository.KEY_DEPARTMENTS)) or []
        return {
            id_: DepartmentInfo(id_, name, faculty) for id_, name, faculty in data
        }

    def get_department_name(self, department_id: str) -> Optional[str]:
        key = f'{Repository.KEY_DEPARTMENT_RANGE_PREFIX}{department_id}'
        value = self._redis_store.get(key)

        if value is None:
            return None

        department_info = loads(value)
        return department_info[0]

    def get_department_date_range(self, department_id: str, season: str) -> Optional[DateRange]:
        key = f'{Repository.KEY_DEPARTMENT_RANGE_PREFIX}{department_id}'
        return self._get_date_range(key, season)

    def update_groups_info(self, groups: Sequence[GroupInfo], date_ranges: Dict[str, Dict[str, list]],
                           force=False):
        if self._redis_store.exists(Repository.KEY_GROUPS) and not force:
            return

        groups_dict = {
            group_info.group_id: group_info for group_info in groups
        }

        items = {Repository.KEY_GROUPS: dumps(groups)}

        for group_id, ranges in date_ranges.items():
            name = groups_dict[group_id].group
            autumn = [] if len(ranges['autumn']) == 0 else ranges['autumn'][-1]
            spring = [] if len(ranges['spring']) == 0 else ranges['spring'][-1]

            items[f'{Repository.KEY_RANGE_PREFIX}{group_id}'] = dumps((name, autumn, spring))

        self._redis_store.mset(items)

    def update_departments_info(self, departments: Sequence[DepartmentInfo], date_range: Dict[str, Dict[str, list]],
                                force=False):
        if self._redis_store.exists(Repository.KEY_DEPARTMENTS) and not force:
            return

        departments_dict = {
            department_info.department_id: department_info for department_info in departments
        }

        items = {Repository.KEY_DEPARTMENTS: dumps(departments)}

        for department_id, ranges in date_range.items():
            name = departments_dict[department_id].department
            if len(ranges['autumn']) == 0:
                autumn = []
            else:
                autumn = self._get_nearest_range(get_moscow_today(), ranges['autumn'])
            if len(ranges['spring']) == 0:
                spring = []
            else:
                spring = self._get_nearest_range(get_moscow_today(), ranges['spring'])

            items[f'{Repository.KEY_DEPARTMENT_RANGE_PREFIX}{department_id}'] = \
                dumps((name, autumn, spring))

        self._redis_store.mset(items)

    def drop_all(self):
        self._redis_store.flushdb()

    @staticmethod
    def _get_nearest_range(today: date, ranges: Sequence[DateRange]):
        for range_ in reversed(ranges):
            if as_date(range_.first) <= today:
                return range_
        else:
            return ranges[0]

    def _get_date_range(self, key: str, season: str) -> Optional[DateRange]:
        _, autumn, spring = loads(self._redis_store.get(key))

        if season == 'autumn':
            range_ = autumn
        else:
            range_ = spring

        if len(range_) != 0:
            return DateRange(*range_)
        else:
            return None


def get_repository():
    if 'repository' not in g:
        g.repository = Repository(databases.redis)

    return g.repository


__all__ = ['get_repository', 'Repository']
