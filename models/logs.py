from utils.mongodb_config import get_collection
from datetime import datetime

_collection = get_collection('logs')


def insert_one(req_path: str):
    _collection.insert_one({
        'path': req_path,
        'date': datetime.now()
    })