from typing import List
from utils.groups_info import GroupInfo


# TODO: Add docstring
def groups_info_to_dict(documents: List[GroupInfo], by_faculty: bool = False) -> dict:
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
