from typing import List
from utils.groups_info import GroupInfo


# TODO: Add docstring
def groups_info_to_list(documents: List[GroupInfo], by_faculty: bool = False) -> List[dict]:
    if by_faculty:
        faculties = {document.faculty for document in documents}
        return [
            {
                'faculty': faculty,
                'groups': [
                    {
                        'id': document.group_id,
                        'name': document.group
                    }
                    for document in documents if document.faculty == faculty
                ]
            }
            for faculty in faculties
        ]
    else:
        return [
            {
                'id': document.group_id,
                'name': document.group
            }
            for document in documents
        ]
