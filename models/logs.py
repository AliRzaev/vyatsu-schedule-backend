from config.mongodb import get_collection
from datetime import datetime

_collection = get_collection('logs')


def insert_one(req_path: str, useragent: str):
    _collection.insert_one({
        'path': req_path,
        'useragent': useragent,
        'date': datetime.now()
    })
