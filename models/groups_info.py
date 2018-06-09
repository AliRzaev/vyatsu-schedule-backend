from utils.db_config import get_collection
from typing import Optional, List
from pymongo import ReplaceOne

_collection = get_collection('groups_info')


def find_group_by_id(group_id: str) -> Optional[dict]:
    document = _collection.find_one(
        filter={
            'groupId': group_id
        }
    )

    return document


def upsert_documents(documents: List[dict]):
    operations = [
        ReplaceOne(
            {'groupId': document['groupId']},
            document, upsert=True) for document in documents
    ]

    _collection.bulk_write(operations, ordered=False)


def find_all() -> List[dict]:
    return _collection.find()
