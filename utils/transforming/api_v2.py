from typing import List, Dict, Iterable
from utils.groups_info import GroupInfo


def groups_info_to_list(documents: List[GroupInfo],
                        by_faculty: bool = False) -> List[dict]:
    """
    Transform groups information into form specified by API 2
    :param documents: list of group information items
    :param by_faculty: group student groups by faculty
    :return: groups information as JSON-like array
    """

    def info_to_dict(item: GroupInfo) -> Dict[str, str]:
        return {
            'id': item.group_id,
            'name': item.group
        }

    def filter_by_faculty(faculty: str,
                          items: List[GroupInfo]) -> Iterable[GroupInfo]:
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
