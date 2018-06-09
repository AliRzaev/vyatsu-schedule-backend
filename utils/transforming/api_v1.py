from typing import List


def groups_info_to_dict(documents: List[dict], by_faculty: bool = False) -> dict:
    if by_faculty:
        _dict = dict()
        for document in documents:
            faculty_name = document['faculty']
            group_name = document['group']
            group_id = document['groupId']

            if faculty_name not in _dict:
                _dict[faculty_name] = dict()

            _dict[faculty_name][group_name] = group_id
        return _dict
    else:
        return {
            document['group']: document['groupId']
            for document in documents
        }
