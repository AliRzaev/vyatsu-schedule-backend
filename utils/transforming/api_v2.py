from typing import List
from utils.groups_info import GroupInfo


def groups_info_to_list(documents: List[GroupInfo],
                        by_faculty: bool = False) -> List[dict]:
    """
    Transform groups information into form specified by API 2
    :param documents: list of group information items
    :param by_faculty: group student groups by faculty
    :return: groups information as JSON-like array
    """
    if by_faculty:
        faculties = {document.faculty for document in documents}
        return [{
            'faculty': faculty,
            'groups': [{
                'id': document.group_id,
                'name': document.group
            } for document in documents if document.faculty == faculty]
        } for faculty in faculties]
    else:
        return [{
            'id': document.group_id,
            'name': document.group
        } for document in documents]
