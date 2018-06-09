from typing import List


def groups_info_to_list(documents: List[dict], by_faculty: bool = False) -> List[dict]:
    if by_faculty:
        faculties = {document['faculty'] for document in documents}
        return [
            {
                'faculty': faculty,
                'groups': [
                    {
                        'id': document['groupId'],
                        'name': document['group']
                    }
                    for document in documents if document['faculty'] == faculty
                ]
            }
            for faculty in faculties
        ]
    else:
        return [
            {
                'id': document['groupId'],
                'name': document['group']
            }
            for document in documents
        ]
