from collections import defaultdict
from functools import lru_cache
from typing import Tuple

from utils.extractors import GroupInfo


@lru_cache()
def groups_info_to_dict(documents: Tuple[GroupInfo, ...],
                        by_faculty: bool = False) -> dict:
    """
    Transform information about groups into form specified by API 1.

    :param documents: list of GroupInfo objects
    :param by_faculty: group student groups by faculty
    :return: the information about groups as JSON-like object
    """
    if by_faculty:
        dict_ = defaultdict(dict)
        for document in documents:
            faculty_name = document.faculty
            group_name = document.group
            group_id = document.group_id

            dict_[faculty_name][group_name] = group_id
        return dict_
    else:
        return {
            document.group: document.group_id
            for document in documents
        }
