from utils.mongodb_config import get_collection
from typing import Optional, List
from pymongo import ReplaceOne

_collection = get_collection('schedule_ranges')


def find_by_group_and_season(group_id: str, season: str) -> Optional[dict]:
    document = _collection.find_one(
        filter={
            'groupId': group_id,
            'season': season
        }
    )

    return document


def upsert_documents(documents: List[dict]):
    operations = [
        ReplaceOne(
            filter={
                'groupId': document['groupId'],
                'season': document['season']
            },
            replacement=document,
            upsert=True
        ) for document in documents
    ]

    _collection.bulk_write(operations, ordered=False)


def delete_all():
    _collection.drop()
