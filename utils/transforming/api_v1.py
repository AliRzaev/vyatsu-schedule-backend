from functools import lru_cache
from typing import Tuple

from utils.groups_info import GroupInfo


@lru_cache()
def groups_info_to_dict(documents: Tuple[GroupInfo, ...],
                        by_faculty: bool = False) -> dict:
    """
    Transform groups information into form specified by API 1
    :param documents: list of group information items
    :param by_faculty: group student groups by faculty
    :return: groups information as JSON-like object
    """
    if by_faculty:
        dict_ = dict()
        for document in documents:
            faculty_name = document.faculty
            group_name = document.group
            group_id = document.group_id

            if faculty_name not in dict_:
                dict_[faculty_name] = dict()

            dict_[faculty_name][group_name] = group_id
        return dict_
    else:
        return {
            document.group: document.group_id
            for document in documents
        }
