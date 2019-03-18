from functools import lru_cache
from typing import List, Dict, Iterable, Tuple

from utils.groups_info import GroupInfo, DepartmentInfo


@lru_cache()
def groups_info_to_list(documents: Tuple[GroupInfo, ...],
                        by_faculty: bool = False) -> List[dict]:
    """
    Transform information about groups into form specified by API 2.

    :param documents: list of GroupInfo objects
    :param by_faculty: group student groups by faculty
    :return: the information about groups as JSON-like array
    """

    def info_to_dict(item: GroupInfo) -> Dict[str, str]:
        return {
            'id': item.group_id,
            'name': item.group
        }

    def filter_by_faculty(faculty: str,
                          items: Tuple[GroupInfo, ...]) -> Iterable[GroupInfo]:
        return filter(lambda info: info.faculty == faculty, items)

    if by_faculty:
        faculties = {document.faculty for document in documents}
        return [{
            'faculty': faculty,
            'groups': sorted(map(info_to_dict,
                                 filter_by_faculty(faculty, documents)),
                             key=lambda item: item['name'])
        } for faculty in sorted(faculties)]
    else:
        return sorted(map(info_to_dict, documents),
                      key=lambda item: item['name'])


@lru_cache()
def departments_info_to_list(documents: Tuple[DepartmentInfo, ...],
                             by_faculty: bool = False) -> List[dict]:
    """
    Transform information about departments into form specified by API 2.

    :param documents: list of DepartmentInfo objects
    :param by_faculty: group departments by faculty
    :return: the information about departments as JSON-like array
    """
    def info_to_dict(item: DepartmentInfo) -> Dict[str, str]:
        return {
            'id': item.department_id,
            'name': item.department
        }

    def filter_by_faculty(
            faculty: str,
            items: Tuple[DepartmentInfo, ...]
    ) -> Iterable[DepartmentInfo]:
        return filter(lambda info: info.faculty == faculty, items)

    if by_faculty:
        faculties = {document.faculty for document in documents}
        return [{
            'faculty': faculty,
            'departments': sorted(map(info_to_dict,
                                      filter_by_faculty(faculty, documents)),
                                  key=lambda item: item['name'])
        } for faculty in sorted(faculties)]
    else:
        return sorted(map(info_to_dict, documents),
                      key=lambda item: item['name'])
